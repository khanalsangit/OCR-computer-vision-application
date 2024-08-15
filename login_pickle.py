import pickle
import os
import numpy as np

########## Pickle file Login Details ###########

def new_login_pkl(username : str, 
                password: str,
                ) -> None:
    
    login_param = {
                'username': username, 
                'password':password,
                   }
   
    dir_path = os.getcwd()
    new_pkl_dir = os.path.join(dir_path, 'login.pkl')
    pickle.dump(login_param,open(new_pkl_dir,'wb'))
    
new_login_pkl('unilever','12345')
