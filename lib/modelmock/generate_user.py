import numpy as np
from modelmock.generate_data import provider
import json,time,os
class Main:
    def __init__(self,numbers):
        self.numbers = numbers
    def __str__(self):
        try:
            if self.numbers > 0:
                return str(self.numbers)
            else:
                print("n nhập vào phải lớn hơn 0")
                exit()
        except:
            print( "n nhập vào phải là kiểu số lớn hơn 0")
            exit()
            
    def sum_str(self,list_):
        result = ''
        for i in list_:
            result+=str(i)
        return result
    def user(self,int_):
        out = ''
        for i in range(int_):
            out+=np.random.choice(provider.header)+np.random.choice(provider.prefix)
        return out
    def numbers_tail(self,int_):
        out = ''
        for i in range(int_):
            out+=np.random.choice(provider.tailer)
        return out
    def free_name(self,key=None):
        def sortcut(str_):
            if str_[0] == " ":
                return str_[1:]
            else:
                return str_
        if key == None :
            key = np.random.choice(["F","M"])
        if key == "F":
            return sortcut(' '.join([" ".join(np.random.choice(provider.first_names_female,np.random.randint(2))),np.random.choice(provider.middle_name)," ".join(np.random.choice(provider.last_names,np.random.randint(1,2)))]))
        elif key == "M":
            return sortcut(' '.join([" ".join(np.random.choice(provider.first_names_male,np.random.randint(2))),np.random.choice(provider.middle_name)," ".join(np.random.choice(provider.last_names,np.random.randint(1,2)))]))
    def free_email(self):
        return self.user(np.random.randint(1,8))+self.numbers_tail(np.random.randint(1,6))+'@'+np.random.choice(provider.free_email_domains)
    def free_phone(self):
        return np.random.choice(provider.phone)+self.sum_str(np.random.choice(10,8).tolist())
    def check_unique(self):
        try:
            try:
                if not os.path.exists('users'):
                    os.mkdir('users')
                else:
                    pass
            except Exception as e:
                os.mkdir('users')
                print(e)
            lst_users = os.listdir('users')
            if '.DS_Store' in lst_users:
                lst_users.remove('.DS_Store')
            else:
                pass
            names = []
            emails = [] 
            phone_numbers = []
            if len(lst_users)>=1:
                for i in lst_users:
                    with open('users/'+i,'r') as f:
                        data = f.read()
                        json_data = json.loads(data)
                        for i in json_data:
                            size = json_data[i]
                            break
                        for i in range(1,size+1):
                            names.append(json_data['details']['user'+str(i)]['Full name'].encode('utf-8').decode('utf-8'))
                            emails.append(json_data['details']['user'+str(i)]['Email'])
                            phone_numbers.append(json_data['details']['user'+str(i)]['Phone number'])
            return names,emails,phone_numbers
        except Exception as e:
            print(e)
    def generation(self):
        # try:
        #     names,emails,phone_numbers = self.check_unique()
        # except:
        #     names,emails,phone_numbers= [],[],[]
        names,emails,phone_numbers= [],[],[]
        namess,emailss,phone_numberss= [],[],[]
        for i in range(self.numbers):
            name = self.free_name()
            namess.append(name)
            while 1:
                email = self.free_email()
                if (email not in emails) and (email not in emailss):
                    emailss.append(email)
                    while 1:
                        phone_number = self.free_phone()
                        if (phone_number not in phone_numbers) and (phone_number not in phone_numberss):
                            phone_numberss.append(phone_number)
                            break
                        else:
                            pass
                    break
                else:
                    pass
        dict_={}
        dic = {
                str(time.localtime(time.time()).tm_mday)+'/'+\
                str(time.localtime(time.time()).tm_mon)+'/'+\
                str(time.localtime(time.time()).tm_year):self.numbers,
                'details':dict_
                }
        for i in range(len(namess)):
            dict_['user'+str(i+1)] = {"Full name":namess[i],"Email":emailss[i],"Phone number":phone_numberss[i]}
        return dic,[namess,emailss,phone_numberss]
    def jsonload(self):
        json_ = json.dumps(self.generation()[0],indent=2).encode('utf-8')
        json_x = json_.decode('utf-8')
        return json_x
    def Savedata(self):
        data = self.jsonload()
        i = 0
        while 1:
            try:

                if not os.path.exists('users/users_'+str(time.localtime(time.time()).tm_mday)+'_'+\
                    str(time.localtime(time.time()).tm_mon)+'_'+\
                    str(time.localtime(time.time()).tm_year)+f'_{i}.json'):
                    with open('users/users_'+str(time.localtime(time.time()).tm_mday)+'_'+\
                            str(time.localtime(time.time()).tm_mon)+'_'+\
                            str(time.localtime(time.time()).tm_year)+f'_{i}.json','a') as f:
                        f.write('\n'+data)
                        break
                else:
                    i+=1
            except:
                pass
        return True
    def printf(self):
        print(self.jsonload())

if __name__ == "__main__":
    time_start = time.time()
    n=int(input('Input n user : '))
    opject = Main(n) #construction
    print(opject) # __str__ 
    opject.printf() #print(json_output)
    opject.Savedata() #Save data to *.json
    '''
        Save Time computing
    '''
    with open('computational_time.txt','a') as f:
        f.write(f'\nTime computing:{time.time()-time_start}s\tNumbers : {n}')
    print(f'Time computing:{time.time()-time_start}')


