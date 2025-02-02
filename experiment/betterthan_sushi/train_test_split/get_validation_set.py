import sys
from clingo.application import clingo_main, Application
from clingo.script import enable_python
from clingo.symbol import String, Number
from clingo.control import Control
import random
import shutil
import os

enable_python()

class App(Application):
    
    def __init__(self):
        self.users = [] #to be obtained by method save_users
        self.dataset_name = '../dataset_1f_ex2'
        self.gen_files = [("../generation/generation_aso.lp","aso"),\
                          ("../generation/generation_lw.lp","less_weight"),\
                          ("../generation/generation_poset.lp","poset")]
        
        #input files tts.lp
        self.dom_file = "../domain.lp"
        self.exT_file = "../examples_v1.lp"
        self.bkd_file = "../../../backend.lp"
        self.lib_file = "../../../asprin_vL_lib.lp"
        self.find_good_users = "../find_good_users.lp"
        self.score = "../score.lp"
        self.prefs_100 = "../prefs_100.lp"
        self.prefs_10 = "../prefs_10.lp"
        self.indices = []
        self.pref = []
        self.in_files = []
        self.curr_user = 0
        self.curr_gen  = ""
        self.gen_code = []
        self.dom_code = []
        self.exT_code = []
        self.bkd_code = []
        self.lib_code = []
    
  
    def main(self, ctl, files):
        
        def save_users(m=None):
            ans = [y for y in m.symbols(shown=True)]
            for k in ans:
                if k.name == "good_user":
                    self.users.append(str(k.arguments[0]))
            print("Number of users: ", len(self.users))
                    
        def save_model(m=None):
            for idx, i in enumerate(self.gen_files):
                dataset = [y for y in m.symbols(shown=True)]                   
                dir = self.dataset_name + '/validation/user' + str(self.curr_user) + '/' + i[1]
                if os.path.exists(dir):
                    shutil.rmtree(dir)
                os.makedirs(dir)
                with open(dir + "/validation_set.lp", "w") as f:
                    f.write("%current gen file is: " + str(i) + ".\n")
                    f.write("%current user number is: " + str(self.curr_user) + ".\n")
                    
                    f.write("#program examples.\n")
                    for k in dataset:
                        if k.name == "pref" and str(k.arguments[2]) == str(0):
                            f.write(str(k) + ".\n")
                        
                    f.writelines(self.dom_code)
                    f.writelines(self.exT_code)
                    f.writelines(self.bkd_code)
                    f.writelines(self.lib_code)
            return False


        self.in_files = files
                
        for i in self.gen_files:
            with open(i[0],'r') as f:
                tmp = f.readlines()
                self.gen_code.append(tmp)
                
        with open(self.dom_file,'r') as f:
            self.dom_code = f.readlines()
        
        with open(self.exT_file,'r') as f:
            self.exT_code = f.readlines()
        
        with open(self.bkd_file,'r') as f:
            self.bkd_code = f.readlines()
            
        with open(self.lib_file,'r') as f:
            self.lib_code = f.readlines()
        
        ctl = Control()
        ctl.load(self.find_good_users)
        ctl.load(self.score)
        ctl.load(self.prefs_100)
        ctl.ground([("base", [])], context=self)
        ctl.solve(on_model=save_users)
        
        for i in self.users:
            self.curr_user= i
            ctl = Control()
            
            ctl.load(self.prefs_10)
            for path in self.in_files:
                ctl.load(path)
            if not self.in_files:
                ctl.load("-")
            prg = "user(" + str(i) + ")."
            ctl.add("base",[],prg)
            ctl.add("base",[],"#show.")   
            ctl.add("base",[],"#show pref/3.")
            ctl.ground([("base", [])], context=self)    
            
            ctl.solve(on_model=save_model)
        
if __name__ == "__main__":
    clingo_main(App(), sys.argv[1:])
