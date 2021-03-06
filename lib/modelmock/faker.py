#!/usr/bin/env python

import random
from modelmock.generate_user import Main
from modelmock.utils import (
  array_random_split,
  chunkify,
  number_to_id,
  generate_ids,
  shuffle_nodes,
  list_to_dict,
  flatten_sub_dict,
  flatten_sub_list,
  random_fixed_sum_array,
)

# [BEGIN generate_agents()]

def generate_agents(total_agents, level_mappings, subpath='record'):
  _records = shuffle_nodes(
    Main(total_agents).generate_user_info(
      flatten_sub_dict(
        expand_treemap(
          assign_levels(None,
            indices=list(shuffle_nodes(generate_ids(total_agents, 'A'))),
            levels=level_mappings)
        )
      )
    )
  )
  if isinstance(subpath, str):
    return map(lambda item: { subpath: item }, _records)
  else:
    return _records

def assign_levels(super_id, indices, levels):
  if not isinstance(indices, list):
    raise TypeError('indices is invalid')

  ret = []

  if not isinstance(indices, list) or len(indices) == 0:
    return ret
  if isinstance(levels, list) and len(levels) > 0:
    current = levels[0]
    levels = levels[1:]
    if len(levels) == 0:
      for i in indices:
        item = dict(
          level=current['level'],
          index=i,
          super=super_id
        )
        ret.append(item)
    else:
      # determines the number of branches
      if 'count' in current:
        _count = current['count']
      else:
        _min = current['min'] if 'min' in current else 0
        _max = current['max'] if 'max' in current else len(indices)
        _count = random.randint(_min, _max)
      # no any branch of this level
      if _count == 0:
        return assign_levels(super_id, indices, levels)
      # split the children
      group_len = _count if _count < len(indices) else len(indices)
      child_group = array_random_split(indices, group_len)
      for child in child_group:
        first_index = child[0]
        subchild = child[1:]
        ret.append(dict(
          level=current['level'],
          index=first_index,
          super=super_id
        ))
        ret = ret + assign_levels(first_index, subchild, levels = levels)
  return ret


def expand_treemap(nodes):
  _lkup = list_to_dict(nodes)
  for node in nodes:
    node['refs'] = dict()
    node['refs'][node['level']] = node['index']

    _super_id = node['super']
    if _super_id is None:
      continue

    _super = _lkup[_super_id]
    _super_refs = _super['refs']

    for ref_label in _super_refs.keys():
      node['refs'][ref_label] = _super_refs[ref_label]

  return nodes

# [END generate_agents()]


# [BEGIN generate_contracts()]

def generate_contracts(contract_price, total_contracts, total_agents, unit, prefix='CONTR', flatten=True, chunky=None):
  # estimate the revenue ~ price * total
  revenue = contract_price * total_contracts
  # randomize the prices (length: total_contracts)
  prices = random_fixed_sum_array(revenue, total_contracts)
  # generate each contracts
  contrs = list(map(lambda idx, price: generate_contract(idx, price, unit, prefix=prefix, flatten=flatten), range(total_contracts), prices))
  # contrs = list(map(lambda x: generate_contract(x[0], x[1], unit, prefix, flatten), enumerate(prices)))
  
  # assign the purchases to agents
  _purchases = assign_purchases(contrs, total_agents)

  _chunks = _purchases
  if chunky is not None:
    if chunky <= 0:
      # randomize number of contracts per chunk
      num_contracts_per_chunk = random_fixed_sum_array(total_contracts, total_agents)
      # splits contracts list into chunks
      _chunks = []
      start = 0
      for n in num_contracts_per_chunk:
        _chunks.append(contrs[start:start + n])
        start = start + n
      # return the chunks
      return _chunks
    else:
      return chunkify(_purchases, chunky)

  return _purchases


def generate_contract(idx, price, unit, prefix='C', max_extras=5, flatten=True, extra_generator=None):
    num_extras = random.randint(1, max_extras)
    if extra_generator is None:
      extras = []
      for idx_extras in range(num_extras):
        extras.append(dict(
          fare = random.randint(1,5) * unit,
          type = random.randint(1,3),
          duration = random.randint(1, 12),
        ))
    else:
      extras = map(extra_generator, range(num_extras))
    _contract = dict(id=number_to_id(idx, prefix, 6), fyp=price * unit, extras=extras)
    if flatten:
      return flatten_sub_list(_contract)
    return _contract


def assign_purchases(contracts, total_agents):
  # randomize number of contracts per agents
  num_contracts_per_agents = random_fixed_sum_array(len(contracts), total_agents)

  start = 0
  for i in range(len(num_contracts_per_agents)):
    for j in range(num_contracts_per_agents[i]):
      contracts[start + j]['agent_id'] = number_to_id(i)
    start = start + num_contracts_per_agents[i]

  return contracts

# [END generate_contracts()]
