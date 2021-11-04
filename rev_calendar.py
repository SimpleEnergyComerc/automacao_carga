from datetime import datetime, timedelta


class SINcalendar:
    
    def __init__(self,carga = True):
        '''
        Por padrão --> carga: devolve semanas operativas considerando o padrao do DECOMP: SEMANA do MES + 1 SEMANA MES + 1
        
        '''
        self.carga = carga
        
        return
    
    
    def _rev_datas(self,mes,ano):
        '''
        
        mes -> mes desejado
        ano -> ano desejado
        
        return -> [[data_inicial1,data_final1],[data_inicial2,data_final2],...]
        vetor com as datas iniciais e finais de cada semana
        
        '''
        
        day1 = datetime(ano,mes,1)
        
        if day1.weekday() == 5: #caso seja sabado
            start_day = day1
        else: # caso nao seja sabado, voltar para ultimo sabado
            start_day = day1 - timedelta(days = 7) + timedelta(days = (5 - day1.weekday())%7)
            
            
        v_dates = []
        final_day = start_day + timedelta(days = 6)
        v_dates.append([start_day,final_day])
        while final_day.month == mes:
            start_day = start_day + timedelta(days = 7)
            final_day = start_day + timedelta(days = 6) + timedelta(hours=23, minutes=59, seconds=59 )
            if start_day.month == mes:
                v_dates.append([start_day,final_day])
            
        if self.carga == 0: ## > dropa ultima semana caso nao seja carga, i.e, nao quero primeira semana mes + 1
            v_dates.pop()
            
        return v_dates
     
    def _rev0(self,data):
        '''
        Caso -> data seja rev0, mudar mes, e eventualmente ano
        '''
        days2sexta = (4 - data.weekday())
        sexta = (data + timedelta(days = 7 + days2sexta))
        if data.month != sexta.month: # o mes da semana que vem mudou, RV0
            month = sexta.month
            year = sexta.year
            return month,year

        else:
            return data.month,data.year

        
    
    def _numero_revs(self,mes,ano):
        '''
        mes -> mes desejado
        ano -> ano desejado
        
        return -> ##(int) numero de revs no mes
        
        '''
        dates = self._rev_datas(mes,ano)
        
        return len(dates)
    
    def _dias_revisoes(self,mes,ano):
        '''
        Devolve numero de dias do mes em cada revisao
        
        mes -> mes desejado
        ano -> ano desejado
        
        return -> [int,int...] numero de dias do mes em cada revisao
        
        '''
        
        
        v_dates = self._rev_datas(mes,ano)
        days_count = []
        for semanas in v_dates:
            days = 0
            for i in range(0,(semanas[1] - semanas[0]).days + 1):
                shift = semanas[0] + timedelta(days = i)

                if shift.month == mes:
                    days += 1
            days_count.append(days)
            
        return days_count

    
    def rev_atual(self,data):
        '''
        datetime -> data do dia que ser quer saber a rev + 1
        
        return -> numero da revisao que será lançada no VE (rev atual + 1)
        '''
        

        month,year = self._rev0(data)
        #data = datetime.today()
        print(data)
        dates_v = self._rev_datas(month,year)
        print("-----------------")
        print(month, year)
        print(dates_v)
        print(len(dates_v))
        print(self._dias_revisoes(month, year))
        print('-------------')
        for rev,(x,y) in enumerate(dates_v):
            #print(x,y)
            print(data >= x)
            print(y >= data)
            print(rev, x, y, y.month, data.month, data)
            if rev == 0 and (y.month > data.month) and (data < x) :
                return 0
            if (data >= x) and (y >= data):
                print("Deveria parar aqui")
                break
        print("----------------")
        print(rev + 1)
        return rev + 1

if __name__ == '__main__':
    calendario = SINcalendar()
    x = calendario._numero_revs(11,2021)
    print(x)