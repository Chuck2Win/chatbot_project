# -*- coding: utf-8 -*-

# gpt2 관련 input들 처리하기
# index of words - tokenized되고 encode 된 id들
# token type ids - [0] : question [1] : answer 
# attention mask - [1] : padding 안 된 부분 [0] : padding 된 부분
# label : Quesion이 부정적인 긍정적인지.
# cls position : cls의 위치 (index)
import argparse
from kogpt2.pytorch_kogpt2 import get_pytorch_kogpt2_model
from gluonnlp.data import SentencepieceTokenizer
from kogpt2.utils import get_tokenizer
import pandas as pd

parser = argparse.ArgumentParser(description = '필요한 변수')
# Input data
parser.add_argument('--max_len', default = 64, type = int)
parser.add_argument('--return_file', default = './data/preprocessed_data', type = str)

tok_path = get_tokenizer()
# model, vocab
model, vocab = get_pytorch_kogpt2_model()
# tokenizer
tokenizer = SentencepieceTokenizer(tok_path,  num_best=0, alpha=0)
# bos token, eos token 붙이기
class make_data_set:
    def __init__(self):
        '''
        data : data frame
        data - Q, A 로 구성 
        '''
        data=pd.read_csv('https://raw.githubusercontent.com/songys/Chatbot_data/master/ChatbotData%20.csv',sep=',',header=0)
        # <usr> sentence <cls>
        data['Q_input_id']=data['Q'].apply(lambda i :[vocab['<usr>']]+vocab[tokenizer(i)]+[vocab['<unused0>']])
        # <sys> sentence </s>
        data['A_input_id']=data['A'].apply(lambda i :[vocab['<sys>']]+vocab[tokenizer(i)]+[vocab['</s>']])
        data['cls_position']=None
        Max = args.max_len
        for i in data.index:
            # Q+A의 길이가 Max보다 길면 Q은 -Max//2부터 끝까지.
            if len(data.Q_input_id[i])+len(data.A_input_id[i])>Max:
                data.Q_input_id[i]=data.Q_input_id[i][-(Max//2):]
                data.A_input_id[i]=data.A_input_id[i][:(Max-(Max//2))]
            # data['attention_mask'][i] = [1] * (len(data.Q_input_id[i])+len(data.A_input_id[i]))+[0] * (Max - (len(data.Q_input_id[i])+len(data.A_input_id[i])))
            # data['token_id'][i] = [0] * len(data.Q_input_id[i]) + [1] * (Max-len(data.Q_input_id[i]))
            # classification을 위해서
            data['cls_position'][i] = len(data.Q_input_id[i])-1 
        data['input_id']=data['Q_input_id']+data['A_input_id']
        # pad 하기
        data['input_id']=data['input_id'].apply(lambda j : j+(Max-len(j))*[vocab['<pad>']])
        # <usr> sentence <cls> | <sys> sentence  | <eos> pad ...
        # pad, pad , ... pad,  | sentence, <eos> | pad, pad ...

        data['lm_label']=data['Q_input_id'].apply(lambda i : len(i) * [vocab['<pad>']])+data['A_input_id'].apply(lambda i : i[1:])
        data['lm_label']=data['lm_label'].apply(lambda j : j+(Max-len(j))*[vocab['<pad>']])
        self.data=data

    def return_data_set(self):
        result=self.data.loc[:,['input_id','lm_label','cls_position','label']]#'attention_mask','token_id','cls_position','lm_label','label']]
        return result

if __name__=='__main__':
    args = parser.parse_args()
    max_len = args.max_len
    data=make_data_set().return_data_set()
    data.to_pickle(args.return_file)