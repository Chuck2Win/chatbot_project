# Simple Chatbot  

## Question에 대응되는 Answer를 Generation, Question에 대응되는 Lable 예측

## 1. Dataset

​	Question, answer, label로 구성됨

​	데이터 수 : 11,876건

​	label의 경우, 일상(0), 이별&부정(1), 사랑&긍정(2)

## 2. Model
![AR](https://raw.githubusercontent.com/Chuck2Win/chatbot_project/main/imgs/model.png)  
​	SKT에서 제공하는 Ko GPT2 모델을 활용함. 기존 모델에 classification layer를 추가한 모델

​	question 부분의 마지막 부분에  <mask>로 class를 예측함, 그리고 <usr> question <mask>로 	answer를 generation함  (Multi task learning 진행)

 	그리고 class가 1(이별&부정), 2(사랑&긍정) 일 경우 선별된 play list에서 음악을 추천함

## 3. Result

|       | NLL(L.M) | BCE(CLS) | ACC(CLS) |
| ----- | -------- | -------- | -------- |
| Train | 6.43     | 0.13     | 0.95     |
| Val   | 19.32    | 0.43     | 0.85     |
| Test  | 18.74    | 0.44     | 0.85     |

![AR](https://raw.githubusercontent.com/Chuck2Win/chatbot_project/main/imgs/RESULT1.png)

![AR](https://raw.githubusercontent.com/Chuck2Win/chatbot_project/main/imgs/RESULT2.png)

![AR](https://raw.githubusercontent.com/Chuck2Win/chatbot_project/main/imgs/RESULT3.png)

![AR](https://raw.githubusercontent.com/Chuck2Win/chatbot_project/main/imgs/RESULT4.png)
