"""
A class to read and specific MIPI reports into Pandas dataframes.
Amjad Karim
2nd April 2020
"""

from zeep import Client
from zeep.helpers import serialize_object
import pandas as pd
import datetime as dt


class Mipi:
    """
    A class for downloading reports from National Grids Market Information
    Portal for gas (MIPI). The public api uses a SOAP API.

    :returns: Mipi class

    Usage::

    >>> from mipi import Mipi
    >>> import datetime as dt
    >>> M = Mipi()
    >>> start = dt.date(2020, 1, 1)
    >>> end = dt.date(2020, 4, 1)
    >>> demand = M.get_physical_flows(from_date=start, to_date=end) #

    """

    def __init__(self):
        self.client = Client('http://marketinformation.natgrid.co.uk/MIPIws-public/public/publicwebservice.asmx?wsdl')
        self.error = "No data retrieved. If you're expecting something try reducing the length of the from-to interval"

    def get_data_item(self, data_item, from_date, to_date, latest=False):

        """
        Retrieves MIPI data for each data_item and returns a pandas dataframe.

        Parameters:
        -----------
        from_date: dt.date
        to_date: dt.date
        data_item: str
                   date item to retrieve
        latest: bool
                retrieve the latest value only or all entries.

        Returns:
        --------
        df: pandas dataframe
            containing date items.
        """

        fromDate = from_date.strftime('%Y-%m-%d')
        toDate = to_date.strftime('%Y-%m-%d')
        if latest:
            LatestFlag = 'Y'
        else:
            LatestFlag = 'N'

        dateType = 'GASDAY'
        ApplicableForFlag = 'Y'  # the query is by GAS DAY

        body = {'LatestFlag': f'{LatestFlag}',
                'ApplicableForFlag': f'{ApplicableForFlag}',
                'FromDate': f'{fromDate}',
                'ToDate': f"{toDate}",
                'DateType': f'{dateType}',
                'PublicationObjectNameList': {'string': f'{data_item}'}}

        r = self.client.service.GetPublicationDataWM(body)

        if r is not None:
                data = r[0].PublicationObjectData['CLSPublicationObjectDataBE']
                data_dic = [serialize_object(d) for d in data]
                df = pd.DataFrame(data=data_dic, columns=data_dic[0].keys())
                df['Value'] = pd.to_numeric(df['Value'])
                print("DEBUG", f"{data_item} gathering complete")
                return df
        else:
            print("WARNING", f'No Data for: {data_item}')

    #######################################################
    # Wrapper methods for collecting common data queries
    #######################################################

    def get_sap(self, from_date, to_date, latest=True):
        """
        Returns the System Average Price for those gas days
        :param self:
        :param from_date:
        :param to_date:
        latest: bool
        retrieve the latest value only or all entries.
        :return: pandas dataframe
        """

        report = 'SAP, Actual Day'
        df = self.get_data_item(report, from_date, to_date, latest=latest)
        return df

    def get_physical_flows(self, from_date, to_date, report='DP6', latest=True):
        """

        Returns the physical flow in mcm3 per day for the given date range.
        Presently supports 3 queries.
        'D+1' is the total NTS demand published the day after a gas day
        'D+6' D+6 is published 6 days afterwards and is the final settled value.
        'PS' gets the gas powerstation demamd
        a given gas day but is not final.

        :param report: str 'DP6', 'DP1' or 'PS'
        :param from_date: datetime
        :param to_date: datetime
        :return: pandas dataframe
        """

        if report == 'DP6':
            report = 'Demand Actual, NTS, D+6'

        elif report == 'DP1':
            report = 'Demand Actual, NTS, D+1'

        elif report == 'PS':
            report = 'NTS Volume Offtaken, Powerstations Total'

        df = self.get_data_item(report, from_date, to_date, latest=latest)
        return df
