
import pandas as pd



def cleansing_data(csv_file):
    data = pd.read_csv(csv_file, encoding='utf-8 sig')
    del data["Unnamed: 0"]
    data.drop_duplicates(["City", "District ", "Street", "Name", "PayType", "Price", "BuildType", "etc", "Sold", "Date"],inplace = True)
    # 면적당 가격 계산을 위해 공급면적만 따로 빼준다
    data['Area'] = data.etc.str.split('/').str[0]
    cleanArea = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
            'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
            '가', '나', '다', '라', '마', '바', '사', '아', '자', '차','카','타','파','하','(']
    for item in cleanArea:
        data['Area'] = data.Area.str.split(item).str[0]  
    # 정수형으로 변환
    data['Area'] = pd.to_numeric(data['Area'])
    del data['etc']
    # 보증금 정보만 따로 넣기 + , 제거
    cleanDeposit = []
    for item in data['Price']:
        if '/' in item:
            a = item.split('/',1)[0]
            # 보증금 정보에서 , 제거 (정수형으로 변환하기 위해)
            b = a.replace(',','')
            cleanDeposit.append(b)
        else:
            cleanDeposit.append(0)
    Deposit = []
    # 보증금 정보 정수로 변환
    for item in cleanDeposit:
        if type(item) == str:
            if '억' in item:
                a = item.split('억',1)[0]
                b = item.split('억',1)[1]
                if b == '':
                    Deposit.append(int(a)*100000000)
                else:
                    Deposit.append(int(a)*100000000 + int(b)*10000)
            else:
                Deposit.append(int(item)*10000)
        else:
            Deposit.append(0)
    data['Deposit'] = Deposit
    # 월세 정보에서 , 빼기
    data['Monthly'] = data.Price.str.split('/').str[1]
    data['Monthly'] = data['Monthly'].str.replace(',','')
    # 이후 계산의 편의를 위해 0000을 붙여서 숫자로 변해줌(실제값으로 계산할 수 있게)
    cleanMonthly = []
    for item in data['Monthly']:
        if type(item) == str:
            if '억' in item:
                idx_num = data[data['Monthly'] == item].index
                data = data.drop(idx_num)
            else:
                if len(item) > 3:
                    idx_num = data[data['Monthly'] == item].index
                    data = data.drop(idx_num)
                else:
                    cleanMonthly.append(int(item)*10000)
        else:
            cleanMonthly.append(0)
    data['Monthly'] = cleanMonthly
    # 전세 가격 분리
    cleanCharter = []
    for item in data['Price']:
        if '/' not in item:
            cleanCharter.append(item)
        else:
            cleanCharter.append(0)
    data['Charter'] = cleanCharter

    # 전세 정보에서 , 빼기
    data['Charter'] = data['Charter'].str.replace(',','')

    # 이후 계산의 편의를 위해 정수형으로 변환
    Charter = []
    for item in data['Charter']:
        if type(item) == str:
            if '억' in item:
                a = item.split('억',1)[0]
                b = item.split('억',1)[1]
                if b == '':
                    a = item.split('억',1)[0]
                    if len(a) > 3:
                        idx_num = data[data['Charter'] == item].index
                        data = data.drop(idx_num)
                    else:
                        Charter.append(int(a)*100000000)
                elif '억' in b:
                    idx_num = data[data['Charter'] == item].index
                    data = data.drop(idx_num)
                else:
                    if len(b) > 5:
                        idx_num = data[data['Charter'] == item].index
                        data = data.drop(idx_num)
                    else:
                        Charter.append(int(a)*100000000 + int(b)*10000)
            else:
                if len(item) > 4:
                    idx_num = data[data['Charter'] == item].index
                    data = data.drop(idx_num)
                else:
                    a = int(item)
                    Charter.append(a*10000)
        else:
            Charter.append(0)        
    data['Charter'] = Charter

    del data["Price"]
    
    # zeppelin에서 돌리기위해 영어로 바꿔줌
    data['PayType'] = data['PayType'].str.replace('월세','monthly')
    data['PayType'] = data['PayType'].str.replace('전세','charter')
    data['PayType'] = data['PayType'].str.replace('단기임대','shortRent')
    data['BuildType'] = data['BuildType'].str.replace('원룸','oneRoom')
    data['BuildType'] = data['BuildType'].str.replace('아파트분양권','APT')
    data['BuildType'] = data['BuildType'].str.replace('아파트','APT')
    data['BuildType'] = data['BuildType'].str.replace('단독/다가구','one_mul')
    data['BuildType'] = data['BuildType'].str.replace('빌라','villa')
    data['BuildType'] = data['BuildType'].str.replace('오피스텔분양권','OPT')
    data['BuildType'] = data['BuildType'].str.replace('오피스텔','OPT')
    # 상가주택은 영어로 commercial building이라고 한다 함
    data['BuildType'] = data['BuildType'].str.replace('상가주택','com_build')
    data['Sold'] = data['Sold'].str.replace('확인','Checked')
    data['Sold'] = data['Sold'].str.replace('거래완료','Sold')
    data['Sold'] = data['Sold'].str.replace('실거래일','Estimate')
    data['Sold'] = data['Sold'].str.replace('등록일','Registered')
    data['City'] = data['City'].str.replace('서울시', 'Seoul')
    data['City'] = data['City'].str.replace('경기도', 'Geyong-gi')
    data['City'] = data['City'].str.replace('인천시', 'Incheon')
    

    
    data.drop_duplicates(["City", "District ", "Street", "Name", "PayType", "BuildType", "Sold", "Date", "Area", "Deposit", "Monthly", "Charter"], inplace = True)
    # 최종적으로 데이터를 저장할 장소
    data.to_csv('testClean_3_6.csv', encoding='utf-8-sig') 



cleansing_data("testCrawl_3_2.csv")





