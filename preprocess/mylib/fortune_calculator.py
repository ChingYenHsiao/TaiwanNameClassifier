import pickle
import pandas as pd 

from mylib.Taiwan_name_seperate import GetFirstName
from mylib.Taiwan_name_seperate import GetLastName
from mylib.Taiwan_name_seperate import checkLastName

with open('./data_output/final/specail_word_dict.txt', 'rb') as handle:
    specail_word_dict = pickle.loads(handle.read())
with open('./data_output/final/moe_data_dict.txt', 'rb') as handle:
    moe_data_dict = pickle.loads(handle.read())
    
    
def Get_stroke(word):
    if word in moe_data_dict:
        radical = moe_data_dict[word]['radical']
        if radical==word:
            return int((moe_data_dict[word]['stroke_count']))
        else:
            return int(moe_data_dict[word]['non_radical_stroke_count']) + Get_stroke(radical)
#         if radical in cun_shi_dict and radical !=word:
#             return int((moe_data_dict[word]['stroke_count'])) + cun_shi_dict[radical]
#non_radical_stroke_count
#        else:
#         moe_data_dict[word]['non_radical_stroke_count']
#             return int((moe_data_dict[word]['stroke_count']))
    if word in specail_word_dict:
        return int(specail_word_dict[word]['stroke_count'])
    return -1
    print(word,'get stroke count failed!')
    
    
    
#算天格
def stroke_heaven(LN):
    #天格：
    #單姓	姓氏筆劃加1 	姓「王」	5
    #複姓	姓氏筆劃相加總	姓「司馬」	15
    
    if len(LN)==1:
        return Get_stroke(LN)+1
    if len(LN)==2:
        return Get_stroke(LN[0])+Get_stroke(LN[1])
    
#算人格
def stroke_man(row):
    #人格：
    #單姓	姓氏加名字第一字的筆劃	文  天祥 8
    #複姓	姓氏最後一字加名字第一字的筆劃	司馬  光	16
    
    LN = row['LastName']
    FN = row['FirstName']
    
    if len(LN)==1:
        return Get_stroke(LN)+Get_stroke(FN[0])
    
    if len(LN)==2:
        return Get_stroke(LN[1])+Get_stroke(FN[0])
    
#算地格
def stroke_earth(FN):
    #地格：
    #單名	名字筆劃加1	王  二  3
    #複名	名字的筆劃相加總	文  天祥	15

    
    if len(FN)==1:
        return Get_stroke(FN)+1
    
    if len(FN)==2:
        return Get_stroke(FN[0])+Get_stroke(FN[1])
    
#算外格
def stroke_outside(row):
    #外格：
    # 單姓單名	等於2	項羽，岳飛	2
    # 單姓複名	名字最後一字加1	陶淵明	9
    # 複姓單名	姓氏第一字加1	司馬光	6
    # 複名複名	姓氏第一字加名字最後一字	司馬相如	
    
    LN = row['LastName']
    FN = row['FirstName']
    
    if len(LN)==1 and len(FN)==1:
        return 2
    
    if len(LN)==1 and len(FN)==2:
        return Get_stroke(FN[1])+1
    
    if len(LN)==2 and len(FN)==1:
        return Get_stroke(LN[0])+1
    if len(LN)==2 and len(FN)==2:
        return Get_stroke(LN[0])+Get_stroke(FN[1])
    
#算總格
def stroke_total(row):
    #八十一數之輪動，乃是以八十數為一單位，81起還本歸元 = 1, 如83劃-80=3劃
    #   姓與名字的筆劃全部相加總，如文天祥的總格19。

    LN = row['LastName']
    FN = row['FirstName']
    
    Total = 0 
    for c in LN:
        Total+=Get_stroke(c)
    for c in FN:
        Total+=Get_stroke(c)    
        
    if Total >80:
        Total-=80
    return Total



#三才 天才 人才 地才
def get_talent_type(structure):
    #http://kimochii0511.pixnet.net/blog/post/54323820-%E6%97%A5%E8%A8%98%E4%BA%BA%E7%94%9F----20131126----%E6%96%B0%E7%94%9F%E5%85%92%E5%8F%96%E5%90%8D-(%E4%B8%89%E6%89%8D%E4%BA%94%E6%A0%BC)
    if type(structure)==int:
        talent_type_dict = {1:'木',2:'木',3:'火',4:'火',5:'土',6:'土',7:'金',8:'金',9:'水',0:'水'}
        return talent_type_dict[ structure%10  ]
    else:
        return '不明'
        
def get_stroke_state(structure):
    stroke_state_dict = { 1:'吉', 2:'凶' ,3:'吉',4:'凶' ,5:'吉',6:'吉',7:'吉',8:'吉',9:'凶',10:'凶',11:'吉',12:'凶',
                   13:'吉',14:'凶',15:'吉',16:'吉',17:'吉',18:'吉',19:'凶',20:'凶',21:'吉',22:'凶',23:'吉',24:'吉',
                25:'吉',26:'凶帶吉',27:'吉帶凶',28:'凶',29:'吉',30:'吉帶凶',31:'吉',32:'吉',33:'吉',34:'凶',35:'吉',
                36:'凶',37:'吉',38:'凶帶吉',39:'吉',40:'吉帶凶',41:'吉',42:'吉帶凶',43:'吉帶凶',44:'凶',45:'吉',46:'凶',
                47:'吉',48:'吉',49:'凶',50:'吉帶凶',51:'吉帶凶',52:'吉',53:'吉帶凶',54:'凶',55:'吉帶凶',56:'凶',
                57:'凶帶吉',58:'吉帶凶',59:'凶',60:'凶',61:'吉帶凶',62:'凶',63:'吉',64:'凶',65:'吉',66:'凶',67:'吉',
                    68:'吉' ,69:'凶',
                    70:'凶',71:'吉帶凶',72:'凶',73:'吉',74:'凶',75:'吉帶凶',76:'凶',77:'吉帶凶',
                    78:'吉帶凶',79:'凶',80:'吉帶凶',81:'吉'
                   }
#     for i in stroke_state:
#         print(i,stroke_state[i])
    if structure in stroke_state_dict:
        return stroke_state_dict[structure]
    else:
        return '不明'
        
        
def get_talent_state(three_talent):
    talent_state_dict = { '木木木':'大吉','木木火':'大吉','木木土':'大吉','木木金':'凶多吉少','木木水':'吉多於凶','木火木':'大吉','木火火':'中吉','木火土':'大吉','木火金':'凶多於吉','木火水':'大凶','木土木':'大凶','木土火':'中吉','木土土':'吉','木土金':'吉多於凶','木土水':'大凶','木金木':'大凶','木金火':'大凶','木金土':'凶多於吉','木金金':'大凶','木金水':'大凶','木水木':'大吉','木水火':'凶多於吉','木水土':'凶多於吉','木水金':'大吉','木水水':'大吉','火木木':'大吉','火木火':'大吉','火木土':'大吉','火木金':'凶多於吉','火木水':'中吉','火火木':'大吉','火火火':'中吉','火火土':'大吉','火火金':'大凶','火火水':'大凶','火土木':'吉多於凶','火土火':'大吉','火土土':'大吉','火土金':'大吉','火土水':'吉多於凶','火金木':'大凶','火金火':'大凶','火金土':'吉凶參半','火金金':'大凶','火金水':'大凶','火水木':'凶多於吉','火水火':'大凶','火水土':'大凶','火水金':'大凶','火水水':'大凶','土木木':'中吉','土木火':'中吉','土木土':'凶多於吉','土木金':'大凶','土木水':'凶多於吉','土火木':'大吉','土火火':'大吉','土火土':'大吉','土火金':'吉多於凶','土火水':'大凶','土土木':'中吉','土土火':'大吉','土土土':'大吉','土土金':'大吉','土土水':'凶多於吉','土金木':'凶多於吉','土金火':'凶多於吉','土金土':'大吉','土金金':'大吉','土金水':'大吉','土水木':'凶多於吉','土水火':'大凶','土水土':'大凶','土水金':'吉凶參半','土水水':'大凶','金木木':'凶多於吉','金木火':'凶多於吉','金木土':'凶多於吉','金木金':'大凶','金木水':'凶多於吉','金火木':'凶多於吉','金火火':'吉凶參半','金火土':'吉凶參半','金火金':'大凶','金火水':'大凶','金土木':'中吉','金土火':'大吉','金土土':'大吉','金土金':'大吉','金土水':'吉多於凶','金金木':'大凶','金金木':'大凶','金金土':'大吉','金金金':'中吉','金金水':'中吉','金水木':'大吉','金水火':'凶多於吉','金水土':'吉','金水金':'大吉','金水水':'中吉','水木木':'大吉','水木火':'大吉','水木土':'大吉','水木金':'凶多於吉','水木水':'大吉','水火木':'中吉','水火火':'大凶','水火土':'凶多於吉','水火金':'大凶','水火水':'大凶','水土木':'大凶','水土火':'中吉','水土土':'中吉','水土金':'中吉','水土水':'大凶','水金木':'凶多於吉','水金火':'凶多於吉','水金土':'大吉','水金金':'中吉','水金水':'大吉','水水木':'大吉','水水火':'大凶','水水土':'大凶','水水金':'大吉','金金火':'吉','水水水':'中吉' }
    #talent_state_dict = collections.OrderedDict(sorted(talent_state_dict.items()))   
#     for index,i in enumerate(talent_state_dict):
#         print(index+1,i,talent_state_dict[i])
    if three_talent in talent_state_dict:
        return talent_state_dict[three_talent]
    else:
        return '不明'
        
def test_name_Fortune_telling(name):
    
    
    name_df = pd.DataFrame()
    name_df['name'] = [ name]
    row =  name_df.iloc[0]
    row['LastName'] = GetLastName(name)
    row['FirstName'] = GetFirstName(name)
    print('名字：',name)
    print('五格')
    heaven = stroke_heaven (row['LastName'])
    earth = stroke_earth (row['FirstName'])
    man = stroke_man (row)
    outside = stroke_outside (row)
    total = stroke_total(row)
    
    print('天格：',heaven,get_stroke_state(heaven))
    print('地格：',earth,get_stroke_state(earth))
    print('人格：',man,get_stroke_state(man))
    print('外格：',outside,get_stroke_state(outside))
    print('總格：',total,get_stroke_state(total))
    
    print('三才')
    print('天才:',get_talent_type(heaven) )
    print('人才:',get_talent_type(man))
    print('地才:',get_talent_type(earth))
    three_talent = get_talent_type(heaven) + \
    get_talent_type(man) + get_talent_type(earth)

    print('三才格局：',get_talent_state(three_talent))
    print('')