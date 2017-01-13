from getopt import short_has_arg
from mimify import mime_decode

__author__ = 'Ajay'

import data_db_wrapper
import logging
from decimal import Decimal

TWO_PLACES = Decimal(10) ** -2
THREE_PLACES = Decimal(10) ** -3


class Mathematics():

    def __init__(self):
        self.averages = None
        self.ex_short_range = None
        self.short_range = None
        self.mid_range = None
        self.long_range = None
        self.ex_long_range = None
        self.db_obj = data_db_wrapper.DataDB()
        self.get_averages()
#----------------------------------------------------------------
    def get_averages(self):
        try:
            self.averages = self.db_obj.get_averages()
            self.ex_short_range = int(self.averages['EX_SHORT_TERM']) - 1
            self.short_range = int(self.averages['SHORT_TERM']) - 1
            self.mid_range = int(self.averages['MID_TERM']) - 1
            self.long_range = int(self.averages['LONG_TERM']) - 1
            self.ex_long_range = int(self.averages['EX_LONG_TERM']) - 1
        except Exception, err:
            logging.exception('Exception while fetching all average values from database')
            return
#----------------------------------------------------------------

    def get_recent_data(self, tab_name):
        '''
        Get last extra_long term rows. And se it for further calculation
        '''
        limit = self.averages['EX_LONG_TERM']
        return self.db_obj.get_recent_data(limit - 1, tab_name)
#----------------------------------------------------------------

    def calculate_avg(self, company_details):
        tab_name = company_details['SYMBOL']
        recent_data = self.get_recent_data(tab_name)
        self.db_obj.add_to_all_companies(tab_name)
        data = []

        EX_SHRT_AVG, EX_SHRT_CHNG, EX_SHRT_SIG = self.calculate_ex_short_average(recent_data[:self.ex_short_range], company_details)
        ex_short_details = [EX_SHRT_SIG, EX_SHRT_AVG, EX_SHRT_CHNG]
        if EX_SHRT_SIG == 1:
            self.db_obj.add_to_xshort_buy(tab_name)
        elif EX_SHRT_SIG == 3:
            self.db_obj.add_to_xshort_sell(tab_name)
        #--------------------------------------------------------------------------------------------------------------
        print recent_data[:self.short_range]
        print self.short_range
        SHRT_AVG, SHRT_DIFF, SHRT_CHNG, SHRT_SIG = self.calculate_short_average(recent_data[:self.short_range], company_details)
        short_details = [SHRT_SIG, SHRT_AVG, SHRT_DIFF, SHRT_CHNG]
        print short_details
        if SHRT_SIG == 1:
            self.db_obj.add_to_short_buy(tab_name)
        elif SHRT_SIG == 3:
            self.db_obj.add_to_short_sell(tab_name)
        #--------------------------------------------------------------------------------------------------------------
        MID_AVG, MID_DIFF, MID_CHNG, MID_SIG = self.calculate_mid_average(recent_data[:self.mid_range], company_details)
        mid_details = [MID_SIG, MID_AVG, MID_DIFF, MID_CHNG]
        if MID_SIG == 1:
            self.db_obj.add_to_mid_buy(tab_name)
        elif MID_SIG == 3:
            self.db_obj.add_to_mid_sell(tab_name)
        #--------------------------------------------------------------------------------------------------------------
        LONG_AVG, LONG_DIFF, LONG_CHNG, LONG_SIG = self.calculate_long_average(recent_data[:self.long_range], company_details)
        long_details = [LONG_SIG, LONG_AVG, LONG_DIFF, LONG_CHNG]
        if LONG_SIG == 1:
            self.db_obj.add_to_long_buy(tab_name)
        elif LONG_SIG == 3:
            self.db_obj.add_to_long_sell(tab_name)
        #--------------------------------------------------------------------------------------------------------------
        EX_LONG_AVG, EX_LONG_SIG = self.calculate_ex_long_average(recent_data[:self.ex_long_range], company_details)
        ex_long_details = [EX_LONG_SIG, EX_LONG_AVG]
        if EX_LONG_SIG == 1:
            self.db_obj.add_to_xlong_buy(tab_name)
        elif EX_LONG_SIG == 3:
            self.db_obj.add_to_xlong_sell(tab_name)
        #--------------------------------------------------------------------------------------------------------------
        PIVOT_VALUE, PIVOT_CHNG = self.calculate_pivot(recent_data, company_details)
        pivot_details = [PIVOT_VALUE, PIVOT_CHNG]
        #--------------------------------------------------------------------------------------------------------------
        stochastic = self.calculate_stochastic(recent_data, company_details)
        stochastic_details = [stochastic]
        #--------------------------------------------------------------------------------------------------------------
        mntm, mntm_chng = self.calculate_momentum(recent_data, company_details, SHRT_AVG)
        momentum_details = [mntm, mntm_chng]
        #--------------------------------------------------------------------------------------------------------------
        macd, macd_chng = self.calculate_macd(recent_data[:1],SHRT_AVG, MID_AVG)
        macd_details = [macd, macd_chng]
        #--------------------------------------------------------------------------------------------------------------
        macd_d = self.calculate_macd_d(macd_details, short_details)
        macd_d_details = [macd_d]
        #--------------------------------------------------------------------------------------------------------------
        certus = self.calculate_certus(recent_data[:4],ex_short_details, short_details, mid_details, stochastic_details)
        if certus == 1:
            self.db_obj.add_to_certus_buy(tab_name)
        elif certus == 3:
            self.db_obj.add_to_certus_sell(tab_name)
        #--------------------------------------------------------------------------------------------------------------
        velox = self.calculate_velox(recent_data[:3], None, ex_short_details, short_details, mid_details,long_details,  pivot_details, macd_details, stochastic_details)
        if velox == 1:
            self.db_obj.add_to_velox_buy(tab_name)
        elif velox == 3:
            self.db_obj.add_to_velox_sell(tab_name)
        if certus == 1 and velox == 1:
            self.db_obj.add_to_certus_velox_buy(tab_name)
        elif certus == 3 and velox == 3:
            self.db_obj.add_to_certus_velox_sell(tab_name)

        #--------------------------------------------------------------------------------------------------------------
        #futuro = self.calculate_futuro(ex_short_details, short_details, mid_details,  pivot_details, recent_data[:2])
        futuro = self.calculate_futuro(recent_data[:3], pivot_details, momentum_details, ex_short_details, short_details,mid_details, long_details, stochastic_details)
        if futuro == 1:
            self.db_obj.add_to_futuro_buy(tab_name)
            if velox == 1:
                self.db_obj.add_to_futuro_velox_buy(tab_name)
            if certus == 1:
                self.db_obj.add_to_certus_futuro_buy(tab_name)
        elif futuro == 3:
            self.db_obj.add_to_futuro_sell(tab_name)
            if velox == 3:
                self.db_obj.add_to_futuro_velox_sell(tab_name)
            if certus == 3:
                self.db_obj.add_to_certus_futuro_sell(tab_name)
        #--------------------------------------------------------------------------------------------------------------
        data.extend(short_details)
        data.extend(mid_details)
        data.extend(long_details)
        data.extend([certus, velox, futuro])  # Here nexus and velocita will come. Calculation still remaining
        data.extend(pivot_details)
        data.extend(stochastic_details)
        data.extend(momentum_details)
        data.append(int(company_details['TOTTRDQTY']))
        data.append(int(company_details['TOTALTRADES']))
        data.extend(ex_short_details)
        data.extend(ex_long_details)
        data.extend(macd_details)
        data.extend(macd_d_details)
        return data
#-----------------------------------------------------------------------------------------------------------------------

    def calculate_ex_short_average(self, ex_short_list_dict, company_details):
        total_val = 0
        ex_short_term_average = 0
        if len(ex_short_list_dict) == self.ex_short_range:
            for row in ex_short_list_dict:
                if row:
                    total_val = total_val + row['CLOSE_PRICE']

            total_val += Decimal(company_details['CLOSE']).quantize(TWO_PLACES)

            if total_val:
                ex_short_term_average = Decimal(total_val / (len(ex_short_list_dict) + 1), 2).quantize(TWO_PLACES)

            last_ex_short_average = ex_short_list_dict[0]['EX_SHRT_AVG']
            if last_ex_short_average:
                difference = ex_short_term_average - last_ex_short_average
                change = Decimal((difference * 100) / ex_short_term_average).quantize(TWO_PLACES)

                if change >= 0:
                    if ex_short_list_dict[0]['EX_SHRT_SIG'] == 1:
                        ex_short_signal = 2
                    elif ex_short_list_dict[0]['EX_SHRT_SIG'] == 2:
                        ex_short_signal = 2
                    elif ex_short_list_dict[0]['EX_SHRT_SIG'] == 3 or ex_short_list_dict[0]['EX_SHRT_SIG'] == 4:
                        ex_short_signal = 1
                    else:
                        ex_short_signal = 1
                else:
                    if ex_short_list_dict[0]['EX_SHRT_SIG'] == 1:
                        ex_short_signal = 3
                    elif ex_short_list_dict[0]['EX_SHRT_SIG'] == 2:
                        ex_short_signal = 3
                    elif ex_short_list_dict[0]['EX_SHRT_SIG'] == 3 or ex_short_list_dict[0]['EX_SHRT_SIG'] == 4:
                        ex_short_signal = 4
                    else:
                        ex_short_signal = 3
                return ex_short_term_average, change, ex_short_signal

        return ex_short_term_average, 0, None
        pass
#-----------------------------------------------------------------------------------------------------------------------

    def calculate_short_average(self, short_list_dict, company_details):
        total_val = 0
        short_term_average = 0
        short_signal = None
        short_diff = 0
        if len(short_list_dict) == self.short_range:
            for row in short_list_dict:
                if row:
                    total_val = total_val + row['CLOSE_PRICE']

            total_val += Decimal(company_details['CLOSE']).quantize(TWO_PLACES)

            if total_val:
                short_term_average = Decimal(total_val / (len(short_list_dict) + 1), 2).quantize(TWO_PLACES)
            last_short_average = short_list_dict[0]['SHRT_AVG']
            if last_short_average:
                difference = short_term_average - last_short_average
                change = Decimal((difference * 100) / short_term_average).quantize(TWO_PLACES)

                if change >= 0:
                    if short_list_dict[0]['SHRT_SIG'] == 1:
                        short_signal = 2
                    elif short_list_dict[0]['SHRT_SIG'] == 2:
                        short_signal = 2
                    elif short_list_dict[0]['SHRT_SIG'] == 3 or short_list_dict[0]['SHRT_SIG'] == 4:
                        short_signal = 1
                    else:
                        short_signal = 1
                else:
                    if short_list_dict[0]['SHRT_SIG'] == 1:
                        short_signal = 3
                    elif short_list_dict[0]['SHRT_SIG'] == 2:
                        short_signal = 3
                    elif short_list_dict[0]['SHRT_SIG'] == 3 or short_list_dict[0]['SHRT_SIG'] == 4:
                        short_signal = 4
                    else:
                        short_signal = 3
                short_diff = short_term_average - short_list_dict[0]['SHRT_AVG']
                return short_term_average, abs(short_diff), change, short_signal

        return short_term_average, 0, 0, None
#-----------------------------------------------------------------------------------------------------------------------

    def calculate_mid_average(self, mid_list_dict, company_details):
        total_val = 0
        mid_term_average = 0
        mid_signal = None
        mid_diff = 0
        if len(mid_list_dict) == self.mid_range:
            for row in mid_list_dict:
                if row:
                    total_val += Decimal(row['CLOSE_PRICE'])

            total_val += Decimal(company_details['CLOSE']).quantize(TWO_PLACES)

            if total_val:
                mid_term_average = Decimal(total_val / (len(mid_list_dict) + 1), 2).quantize(TWO_PLACES)

            last_mid_average = mid_list_dict[0]['MID_AVG']
            if last_mid_average:
                difference = mid_term_average - last_mid_average
                change = Decimal((difference * 100) / mid_term_average).quantize(TWO_PLACES)

                if change >= 0:
                    if mid_list_dict[0]['MID_SIG'] == 1:
                        mid_signal = 2
                    elif mid_list_dict[0]['MID_SIG'] == 2:
                        mid_signal = 2
                    elif mid_list_dict[0]['MID_SIG'] == 3 or mid_list_dict[0]['MID_SIG'] == 4:
                        mid_signal = 1
                    else:
                        mid_signal = 1
                else:
                    if mid_list_dict[0]['MID_SIG'] == 1:
                        mid_signal = 3
                    elif mid_list_dict[0]['MID_SIG'] == 2:
                        mid_signal = 3
                    elif mid_list_dict[0]['MID_SIG'] == 3 or mid_list_dict[0]['MID_SIG'] == 4:
                        mid_signal = 4
                    else:
                        mid_signal = 3
                mid_diff = mid_term_average - mid_list_dict[0]['MID_AVG']
                return mid_term_average, abs(mid_diff), change, mid_signal

        return mid_term_average, 0, 0, None
#-----------------------------------------------------------------------------------------------------------------------

    def calculate_long_average(self, long_list_dict, company_details):
        total_val = 0
        long_term_average = 0
        long_signal = None
        long_diff = 0

        if len(long_list_dict) == self.long_range:
            for row in long_list_dict:
                if row:
                    total_val = Decimal(total_val + row['CLOSE_PRICE'])

            total_val += Decimal(company_details['CLOSE']).quantize(TWO_PLACES)

            if total_val:
                long_term_average = Decimal(total_val / (len(long_list_dict) + 1), 2).quantize(TWO_PLACES)

            last_long_average = long_list_dict[0]['LONG_AVG']
            if last_long_average:
                difference = long_term_average - last_long_average
                change = Decimal((difference * 100) / long_term_average).quantize(TWO_PLACES)

                if change >= 0:
                    if long_list_dict[0]['LONG_SIG'] == 1:
                        long_signal = 2
                    elif long_list_dict[0]['LONG_SIG'] == 2:
                        long_signal = 2
                    elif long_list_dict[0]['LONG_SIG'] == 3 or long_list_dict[0]['LONG_SIG'] == 4:
                        long_signal = 1
                    else:
                        long_signal = 1
                else:
                    if long_list_dict[0]['LONG_SIG'] == 1:
                        long_signal = 3
                    elif long_list_dict[0]['LONG_SIG'] == 2:
                        long_signal = 3
                    elif long_list_dict[0]['LONG_SIG'] == 3 or long_list_dict[0]['LONG_SIG'] == 4:
                        long_signal = 4
                    else:
                        long_signal = 3
                long_diff = long_term_average - long_list_dict[0]['LONG_AVG']
                return long_term_average, abs(long_diff), change, long_signal

        return long_term_average, 0, 0, None
#-----------------------------------------------------------------------------------------------------------------------

    def calculate_ex_long_average(self, ex_long_list_dict, company_details):
        total_val = 0
        long_ex_term_average = 0
        ex_long_signal = None
        if len(ex_long_list_dict) == self.ex_long_range:
            for row in ex_long_list_dict:
                if row:
                    total_val = Decimal(total_val + row['CLOSE_PRICE'])

            total_val += Decimal(company_details['CLOSE']).quantize(TWO_PLACES)

            if total_val:
                long_ex_term_average = Decimal(total_val / (len(ex_long_list_dict) + 1), 2).quantize(TWO_PLACES)

            last_ex_long_average = ex_long_list_dict[0]['EX_LONG_AVG']
            if last_ex_long_average:
                difference = long_ex_term_average - last_ex_long_average
                change = Decimal((difference * 100) / long_ex_term_average).quantize(TWO_PLACES)

                if change >= 0:
                    if ex_long_list_dict[0]['EX_LONG_SIG'] == 1:
                        ex_long_signal = 2
                    elif ex_long_list_dict[0]['EX_LONG_SIG'] == 2:
                        ex_long_signal = 2
                    elif ex_long_list_dict[0]['EX_LONG_SIG'] == 3 or ex_long_list_dict[0]['EX_LONG_SIG'] == 4:
                        ex_long_signal = 1
                    else:
                        ex_long_signal = 1
                else:
                    if ex_long_list_dict[0]['EX_LONG_SIG'] == 1:
                        ex_long_signal = 3
                    elif ex_long_list_dict[0]['EX_LONG_SIG'] == 2:
                        ex_long_signal = 3
                    elif ex_long_list_dict[0]['EX_LONG_SIG'] == 3 or ex_long_list_dict[0]['EX_LONG_SIG'] == 4:
                        ex_long_signal = 4
                    else:
                        ex_long_signal = 3
                return long_ex_term_average, ex_long_signal

        return long_ex_term_average, None
#-----------------------------------------------------------------------------------------------------------------------

    def calculate_pivot(self, details, company_details):
        current_pivot = (Decimal(company_details['HIGH']) + Decimal(company_details['LOW']) + Decimal(company_details['CLOSE'])) / 3
        current_pivot = Decimal(current_pivot, 2).quantize(TWO_PLACES)
        try:
            if details[0]:
                last_pivot = details[0]['PIVOT_VALUE']
                if last_pivot:
                    pivot_change = Decimal(((current_pivot - last_pivot) * 100) / current_pivot).quantize(TWO_PLACES)
                    return current_pivot, pivot_change
        except IndexError:
            logging.exception('Exception occurred as this is first entry and list is empty. This can be ignored')
        return current_pivot, 0
#-----------------------------------------------------------------------------------------------------------------------

    def calculate_stochastic(self, details, company_details):
        if len(details) >= 13:
            low_sequence = [item['LOW_PRICE'] for item in details[:12]]
            low_sequence.append(Decimal(company_details['LOW']))
            high_sequence = [item['HIGH_PRICE'] for item in details[:12]]
            high_sequence.append(Decimal(company_details['HIGH']))
            lowest = min(low_sequence)
            highest = max(high_sequence)
            if highest - lowest == 0:
                return None
            stochastic = ((Decimal(company_details['CLOSE']).quantize(TWO_PLACES) - lowest) * 100) / (highest - lowest)
            stochastic = Decimal(stochastic).quantize(TWO_PLACES)
            return stochastic
        else:
            return None

    def calculate_momentum(self, details, company_details, short_avg):
        momentum = 0
        mntm_var = 0
        if len(details) > 8:
            today_close = Decimal(company_details['CLOSE']).quantize(TWO_PLACES)
            ten_day_close = details[8]['CLOSE_PRICE']
            momentum = today_close - ten_day_close
            if details[0]['MNTM']:
                mntm_dif = momentum - details[0]['MNTM']
                mntm_var = Decimal((mntm_dif * 100) / short_avg).quantize(TWO_PLACES)
            return momentum, mntm_var
        else:
            return momentum, mntm_var

    def calculate_macd(self, details, short_avg, mid_avg):
        macd = 0
        if short_avg and mid_avg:
            macd = short_avg - mid_avg
        try:
            if details[0]:
                last_macd = details[0]['MACD']
                if last_macd and macd:
                    macd_change = Decimal(((macd - last_macd) * 100) / short_avg).quantize(TWO_PLACES)
                    return macd, macd_change
        except IndexError:
            logging.exception('Exception occurred as this is first entry and list is empty. This can be ignored')
        return macd, 0

    def calculate_macd_d(self, macd_details, short_details):
        if short_details[0] > 0:
            macd_d_chng = Decimal((macd_details[0] * 100) / short_details[1]).quantize(TWO_PLACES)
            return macd_d_chng

    def calculate_certus(self,details, ex_short_details, short_details, mid_details, stochastic_details):
        if len(details) >= 1:
            if short_details[0] in [4]:
                if ex_short_details[2] >= details[0]['EX_SHRT_CHNG']:
                    if stochastic_details[0] >= details[0]['STOCHASTIC']:
                        if short_details[2] >= (details[0]['SHRT_CHNG'] + Decimal(str(0.4)).quantize(TWO_PLACES)):
                            if mid_details[2] >= (details[0]['MID_CHNG'] - Decimal(str(0.15)).quantize(TWO_PLACES)):
                                return 1
                        if mid_details[2] >= (details[0]['MID_CHNG'] + Decimal(str(0.2)).quantize(TWO_PLACES)):
                            if short_details[2] >= (details[0]['SHRT_CHNG'] - Decimal(str(0.30)).quantize(TWO_PLACES)):
                                return 1
            if short_details[0] in [2]:
                if ex_short_details[2] <= details[0]['EX_SHRT_CHNG']:
                    if stochastic_details[0] <= details[0]['STOCHASTIC']:
                        if short_details[2] <= (details[0]['SHRT_CHNG'] - Decimal(str(0.4)).quantize(TWO_PLACES)):
                            if mid_details[2] <= (details[0]['MID_CHNG'] + Decimal(str(0.15)).quantize(TWO_PLACES)):
                                return 3
                        if mid_details[2] <= (details[0]['MID_CHNG'] - Decimal(str(0.2)).quantize(TWO_PLACES)):
                            if short_details[2] <= (details[0]['SHRT_CHNG'] + Decimal(str(0.30)).quantize(TWO_PLACES)):
                                return 3
            return None
        return None

    def calculate_velox(self, details, futuro, ex_short_details, short_details,mid_details, long_details, pivot_details, macd_details, stochastic_details):
        if len(details) >= 1:
            if short_details[0] == 4:
                if mid_details[2] <= details[0]['MID_DIFF']:
                    if pivot_details[0] > details[0]['PIVOT_VALUE']:
                        return 1
            elif short_details[0] == 2:
                if mid_details[2] <= details[0]['MID_DIFF']:
                    if pivot_details[0] < details[0]['PIVOT_VALUE']:
                        return 3
            else:
                return None
        return None

    def calculate_velox_old(self, details, futuro, ex_short_details, short_details,mid_details, long_details, pivot_details, momentum_details, stochastic_details ):
        if len(details) >= 1:
            universal_condition_ex_short = 0
            universal_condition_short = 0
            last_ex_short_signals = []
            last_short_signals = []

            for item in details[:2]:
                last_ex_short_signals.append(item['EX_SHRT_SIG'])
            for item in details[:2]:
                last_short_signals.append(item['SHRT_SIG'])

            if ex_short_details[0] in [1, 4]:
                universal_condition_ex_short = 1
            elif ex_short_details[0] in [2]:
                if 1 in last_ex_short_signals:
                    universal_condition_ex_short = 1

            if short_details[0] in [1, 4]:
                universal_condition_short = 1
            elif short_details[0] in [2]:
                if 1 in last_short_signals:
                    universal_condition_short = 1

            if universal_condition_short == 1 and universal_condition_ex_short == 1:
                if pivot_details[1] >= 1.4:
                    if ex_short_details[2] >= (details[0]['EX_SHRT_CHNG'] + Decimal(str(0.8)).quantize(TWO_PLACES)) \
                            or short_details[2] >= (details[0]['SHRT_CHNG'] + Decimal(str(0.8)).quantize(TWO_PLACES)) \
                            or ex_short_details[2] >= 0.8 \
                            or short_details[2] >= 0.8:
                        if mid_details[2] >= (details[0]['MID_CHNG'] + Decimal(str(0.5)).quantize(TWO_PLACES)) \
                                or long_details[2] >= (details[0]['LONG_CHNG'] + Decimal(str(0.5)).quantize(TWO_PLACES)) \
                                or mid_details[2] >= 0.5 \
                                or long_details[2] >= 0.5:
                            return 1



            universal_condition_ex_short = 0
            universal_condition_short = 0

            if ex_short_details[0] in [2, 3]:
                universal_condition_ex_short = 2
            elif ex_short_details[0] in [4]:
                if 3 in last_ex_short_signals:
                    universal_condition_ex_short = 2

            if short_details[0] in [2, 3]:
                universal_condition_short = 2
            elif short_details[0] in [4]:
                if 3 in last_short_signals:
                    universal_condition_short = 2

            if universal_condition_short == 2 and universal_condition_ex_short == 2:
                if pivot_details[1] <= -1.4:
                    if ex_short_details[2] <= (details[0]['EX_SHRT_CHNG'] - Decimal(str(0.8)).quantize(TWO_PLACES)) \
                            or short_details[2] <= (details[0]['SHRT_CHNG'] - Decimal(str(0.8)).quantize(TWO_PLACES)) \
                            or ex_short_details[2] <= -0.8 \
                            or short_details[2] <= -0.8:
                        if mid_details[2] <= (details[0]['MID_CHNG'] - Decimal(str(0.5)).quantize(TWO_PLACES)) \
                                or long_details[2] <= (details[0]['LONG_CHNG'] - Decimal(str(0.5)).quantize(TWO_PLACES)) \
                                or mid_details[2] <= -0.5 \
                                or long_details[2] <= -0.5:
                            return 3

    def calculate_futuro(self, details, pivot_details, momentum_details, ex_short_details, short_details,mid_details, long_details, stochastic_details):
        if len(details) >= 1:
            if short_details[0] == 4:
                if short_details[2] <= details[0]['SHRT_DIFF']:
                    if pivot_details[0] > details[0]['PIVOT_VALUE']:
                        return 1
            elif short_details[0] == 2:
                if short_details[2] <= details[0]['SHRT_DIFF']:
                    if pivot_details[0] < details[0]['PIVOT_VALUE']:
                        return 3
            else:
                return None
        return None

    def calculate_futuro_old(self, details, pivot_details, momentum_details, ex_short_details, short_details,mid_details, long_details, stochastic_details):
        if len(details) >= 2:
            universal_condition_ex_short = 0
            universal_condition_short = 0
            last_ex_short_signals = []
            last_short_signals = []

            for item in details[:2]:
                last_ex_short_signals.append(item['EX_SHRT_SIG'])
            for item in details[:2]:
                last_short_signals.append(item['SHRT_SIG'])

            if ex_short_details[0] in [1, 4]:
                universal_condition_ex_short = 1
            elif ex_short_details[0] in [2]:
                if 1 in last_ex_short_signals:
                    universal_condition_ex_short = 1

            if short_details[0] in [1, 4]:
                universal_condition_short = 1
            elif short_details[0] in [2]:
                if 1 in last_short_signals:
                    universal_condition_short = 1

            if universal_condition_short == 1 and universal_condition_ex_short == 1:
                if pivot_details[1] >= 1.4:
                    if mid_details[2] >= 0.5:
                        if long_details[2] >= 0.5:
                            return 1

            universal_condition_ex_short = 0
            universal_condition_short = 0

            if ex_short_details[0] in [2, 3]:
                universal_condition_ex_short = 2
            elif ex_short_details[0] in [4]:
                if 3 in last_ex_short_signals:
                    universal_condition_ex_short = 2

            if short_details[0] in [2, 3]:
                universal_condition_short = 2
            elif short_details[0] in [4]:
                if 3 in last_short_signals:
                    universal_condition_short = 2

            if universal_condition_short == 2 and universal_condition_ex_short == 2:
                if pivot_details[1] <= -1.4:
                    if mid_details[2] <= -0.5:
                        if long_details[2] <= -0.5:
                            return 3

    def check_quantity_traders(self, last, latest):
        latest = int(latest)
        if latest >= 1.4 * last:
            return 1
        return


