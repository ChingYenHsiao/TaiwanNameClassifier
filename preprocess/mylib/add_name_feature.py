import pickle
#Read files

with open('./data_output/graduate/files/specail_word_dict', 'rb') as handle:
    specail_word_dict = pickle.loads(handle.read())
    
with open('./data_output/graduate/files/moe_additional_dict', 'rb') as handle:
    moe_additional_dict = pickle.loads(handle.read())

with open('./data_output/graduate/files/radical_list', 'rb') as handle:
    radical_list = pickle.loads(handle.read())

with open('./data_output/graduate/files/Totalname_list', 'rb') as handle:
    Totalname_list = pickle.loads(handle.read())
    
with open('./data_output/graduate/files/son_in_list', 'rb') as handle:
    son_in_list = pickle.loads(handle.read())
    
with open('./data_output/graduate/files/moe_data_dict', 'rb') as handle:
    moe_data_dict = pickle.loads(handle.read())
    
with open('./data_output/graduate/files/mu_in_list', 'rb') as handle:
    mu_in_list = pickle.loads(handle.read())
    
  
def add_radical_column(character):
    term = Totalname_list[character]
    if term in moe_data_dict:
        #print(term,moe_data_dict[term]['radical'])
        return moe_data_dict[term]['radical'] 
    elif term in specail_word_dict :
        return specail_word_dict[term]['radical']  
        
def add_radical_index_column(radical):
    if radical in radical_list:
        return radical_list.index(radical)
    else:
        #print(radical)
        return -1

def add_pin_in_column(character, mode):
    #mode 1 = sonin
    #mode 2 = muin
    if character==-1:
        return None
    specail_word_pinyin_dic = {'艶':'yàn' ,'鳯':'fèng','恵':'huì','姈':'líng','寳':'bǎo','姫':'jī','鑅':'róng',
                              "玂":"qí","浤":"hóng",'煊':'xuān','斔':'zhōng','琜':'lái','苰':'hóng','玹':'xuán','姵':'pèi','妏':'wèn',
'妘':'yún','珺':'jùn','媗':'xuān','彣':'wén','玹':'xuán','瀞':'jìng','妡':'xīn','琁':'xuán','浤':'hóng','緁':'jī',
'媜':'zhēng','姸':'yán','嬅':'huà','眞':'zhēn','廼':'nǎi','寛':'kuān','秝':'lì','蕥':'yǎ','汯':'hóng','逹':'dá','萓':'yí',
'媃':'róu','孋':'lí','媁':'wěi','祤':'yǔ','媄':'měi','夆':'fēng','蒝':'yuán','嬣':'níng','砡':'yù','芠':'wén',
'姳':'mǐng','蔆':'líng','菈':'lā','鍹':'xuān','榳':'tíng','錤':'jī','憓':'huì','潓':'huì','瓈':'lí','芛':'wěi',
'峮':'qún','鋕':'zhì','姷':'yòu','兪':'yú','瑠':'liú','嫙':'xuán','珅':'shēn','暟':'kǎi','斈':'xué','煐':'yīng','淓':'fāng','瑨':'jìn','嬨':'cí','琹':'qín','珆':'yí','琣':'pěi',
'娪':'wú','荺':'yǔn','爕':'xiè','玶':'píng','鋆':'yún','愼':'shèn','斳':'qín','瑈':'róu','澪':'líng','珦':'xiàng','妶':'xián','姃':'zhēng','薾':'ěr','溎':'guì','琄':'xuàn','琡':'shū','瑭':'táng','嫆':'róng'
                              }
    term = Totalname_list [character ]
    try:
        if term not in moe_data_dict:
            term = HanziConv.toTraditional(term)
            
        if term in moe_data_dict:
#            pin_yin_list = []
#             if len( moe_data_dict[term]['heteronyms'])>1:
#                 for hete in moe_data_dict[term]['heteronyms']:
#                     if 'pinyin' in hete and  moe_data_dict[term]['title']!='啐':
#                         if 'pinyin' not in pin_yin_list and  '（' not  in (hete['pinyin']):
#                             pin_yin_list.append(hete['pinyin'])
            
#             if len(pin_yin_list)>1:
#                 for word_p in pin_yin_list:
#                             #word_p = hete['pinyin']
#                             #if '（' not  in (word_p) and moe_data_dict[term]['title']!='啐': 
#                         for mu in mu_in_list:
#                             if mu in word_p:
#                                 if mode=='sonin':
#                                     #print(word_p[: word_p.index(mu)])
#                                     print('字：',moe_data_dict[term]['title'],'拼音：',word_p)
#                                     #return word_p[: word_p.index(mu)]
#                                     break
#                                 else:
#                                     return mu

            for hete in moe_data_dict[term]['heteronyms']:
                if 'pinyin' in hete and  moe_data_dict[term]['title']!='啐':
                    word_p = hete['pinyin']
                    
                    if '（'  in (hete['pinyin']):
                        if '（讀音）' in hete['pinyin']:
                            word_p = hete['pinyin'].replace('（讀音）','')
                        if '（語音）' in hete['pinyin']:
                            word_p = hete['pinyin'].replace('（語音）','')   
                        if '(' in word_p:
                            print(word_p+"!!")  

                            
                    for mu in mu_in_list:
                        if mu in word_p:
                            if mode=='sonin':
                                return word_p[: word_p.index(mu)]
                            else:
                                return mu                                    
            #找不到字音，看是否是哪個字的異體字
            for hete in moe_data_dict[term]['heteronyms']:
                for define in hete['definitions']:
                    if '異體字' in define['def']:
                        d =  define['def']
                        alt_term = d[  d.index('「')+1 : d.index('」') ]
                        #print(alt_term,term)
                        
                        for hete2 in moe_data_dict[alt_term]['heteronyms']:
                            if 'pinyin' in hete2 and  moe_data_dict[alt_term]['title']!='啐':
                                
                                word_p = hete2['pinyin']
                                if '（'  in (hete2['pinyin']):
                                    if '（讀音）' in hete2['pinyin']:
                                        word_p = hete2['pinyin'].replace('（讀音）','')
                                    if '（語音）' in hete2['pinyin']:
                                        word_p = hete2['pinyin'].replace('（語音）','')   
                                    if '(' in word_p:
                                        print(word_p+"!!")
                                    
                                for mu in mu_in_list:
                                    if mu in word_p:
                                        if mode=='sonin':
                                            return word_p[: word_p.index(mu)]
                                        else:
                                            return mu     
            #print('在字典內但沒有拼音：',term)
        else:
            #print('不在字典內：',term)
            
            if term in specail_word_dict:
                word_p = specail_word_dict[term]['pinyin']
                for mu in mu_in_list:
                    if mu in word_p:
                        if mode=='sonin':
                            return word_p[: word_p.index(mu)]
                        else:
                            return mu   
            else:
                #print('拼音不明：',term)
                if term not in unkown_dict:
                    unkown_dict[term]=1
                else:
                    unkown_dict[term]+=1

#             if len( moe_df[moe_df.字詞名.apply(lambda x: x==term)])>0:
#                 print('不在字典內：',term)
    except Exception as e:
        print (e)
        PrintException() 

def add_pin_in_index_column(pin_yin, mode):
    #mode 1 = sonin
    #mode 2 = muin
    if pin_yin ==None:
        return -1
    try:
        if mode =='muin':
            return mu_in_list.index(pin_yin)
        
        if mode == 'sonin':
            if pin_yin in son_in_list:
                return son_in_list.index(pin_yin)
            else:
                print(pin_yin)

    except Exception as e:
        print (e)
        print (fileName)
        PrintException() 
        

#get the word vectors one by one   
def add_word_vector(vector_model,word,n):
    if word in vector_model.wv:
        return vector_model.wv[word][n]
    else:
        if word in common_dict:
            if common_dict[word] in vector_model.wv:
                return vector_model.wv[common_dict[word]][n]
            else:
                return 0
        else:
            return 0