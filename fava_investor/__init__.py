"""Fava Investor: Investing related reports and tools for Beancount/Fava"""
import datetime

from fava.ext import FavaExtensionBase
from fava.util.date import Interval

from .modules.performance.balances import get_closed_tree_with_value_accounts_only
from .modules.tlh import libtlh
from .modules.assetalloc_class import libassetalloc
from .modules.assetalloc_account import libaaacc
from .modules.cashdrag import libcashdrag
from .common.favainvestorapi import *


class Investor(FavaExtensionBase):  # pragma: no cover
    report_title = "Investor"

    # AssetAllocClass
    # -----------------------------------------------------------------------------------------------------------
    def build_assetalloc_by_class(self, begin=None, end=None):
        accapi = FavaInvestorAPI(self.ledger)
        retval = libassetalloc.assetalloc(accapi, self.config.get('asset_alloc_by_class', {}))
        return retval

    # AssetAllocAccount
    # -----------------------------------------------------------------------------------------------------------
    def build_aa_by_account(self, begin=None, end=None):
        accapi = FavaInvestorAPI(self.ledger)
        # if begin:
        #     tree = Tree(iter_entry_dates(self.ledger.entries, begin, end))
        # else:
        #     tree = self.ledger.root_tree

        return libaaacc.portfolio_accounts(accapi, self.config.get('asset_alloc_by_account', []))

    # Cash Drag
    # -----------------------------------------------------------------------------------------------------------
    def build_cashdrag(self, begin=None, end=None):
        accapi = FavaInvestorAPI(self.ledger)
        return libcashdrag.find_loose_cash(accapi, self.config.get('cashdrag', {}))

    # TaxLossHarvester
    # -----------------------------------------------------------------------------------------------------------
    def query_func(self, sql):
        contents, rtypes, rrows = self.ledger.query_shell.execute_query(sql)
        return rtypes, rrows

    def build_tlh_tables(self, begin=None, end=None):
        return libtlh.get_tables(self.query_func, self.config.get('tlh', {}))

    # Balances
    # -----------------------------------------------------------------------------------------------------------
    def build_balances_tree(self):
        accapi = FavaInvestorAPI(self.ledger)
        return get_closed_tree_with_value_accounts_only(accapi, self.config.get('performance', {}))

