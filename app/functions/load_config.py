import json
def load_config_json(file_name):
    '''
    Open a file_name and try to parse from json forma to dict. If fail return None.
    '''
    try:
        with open(file_name,'r') as f:
            config = json.load(f)
            f.close() 
    except  Exception as e:
            print(str(e),'\n',file_name)
            config = None   
    return config    


def get_bot_is_working_from_config():
    '''
    Gets bot_is_working value from config.json  
    Returns a boolean value True: is working False is not working
    if fails return False
    '''
    ret = False
    config = load_config_json('config.json')
    if config:
        try: 
            ret = bool(config['bot_is_working'])
        except:
            pass    
    return ret        
