# LOANS

OVERVIEW = (
    "*X7 Finance Loan Terms*\n\n"
    "Use `/loans ill001 - ill003` for more details on individual loan contracts\n\n"
    "Loan terms are defined by standalone smart contracts that provide the following:\n\n"
    "1. Loan origination fee\n"
    "2. Loan retention premium fee schedule\n"
    "3. Principal repayment condition/maximum loan duration\n"
    "4. Liquidation conditions and Reward\n"
    "5. Loan duration\n\n"
    "The lending process delegates the loan terms to standalone smart contracts (see whitepaper below for "
    "more details). These loan terms contracts must be deployed, and then “added” or “removed” from the "
    "Lending Pool as “available” loan terms for new loans. The DAO will be able to add or remove these term "
    "contracts.\n\nLoan term contracts may be created by any interested third party, enabling a market "
    "process by which new loan terms may be invented, provided they implement the proper interface."
)

ILL001_NAME = "X7 Initial Liquidity Loan Term (001) - X7ILL001"
ILL002_NAME = "X7 Initial Liquidity Loan Term (002) - X7ILL002"
ILL003_NAME = "X7 Initial Liquidity Loan Term (003) - X7ILL003"


class LoanTerm:
    def __init__(
        self,
        name,
        min_loan,
        max_loan,
        leverage,
        num_repayment_periods,
        num_premium_periods,
        min_loan_duration,
        max_loan_duration,
        loan_origination_fee,
        loan_retention_premium_fee_schedule,
        principal_repayment_condition,
        liquidation_conditions,
        liquidator_reward,
    ):
        self.name = name
        self.min_loan = min_loan
        self.max_loan = max_loan
        self.leverage = leverage
        self.num_repayment_periods = num_repayment_periods
        self.num_premium_periods = num_premium_periods
        self.min_loan_duration = min_loan_duration
        self.max_loan_duration = max_loan_duration
        self.loan_origination_fee = loan_origination_fee
        self.loan_retention_premium_fee_schedule = loan_retention_premium_fee_schedule
        self.principal_repayment_condition = principal_repayment_condition
        self.liquidation_conditions = liquidation_conditions
        self.liquidator_reward = liquidator_reward

    def generate_terms(self):
        return f"""
    > Min Loan: {self.min_loan} ETH
    > Max Loan: {self.max_loan} ETH
    > Leverage: {self.leverage} leverage
    > Number of repayment periods: {self.num_repayment_periods}
    > Number of premium periods: {self.num_premium_periods}
    > Min Loan Duration: {self.min_loan_duration}
    > Max Loan Duration: {self.max_loan_duration}\n
    > Loan Origination Fee:\n{self.loan_origination_fee} of borrowed capital, payable within the transaction for adding initial liquidity\n
    > Loan Retention Premium Fee Schedule:\n{self.loan_retention_premium_fee_schedule} of borrowed capital payable by the end of each quarter of the loan term for a total retention premium fee of 25% of borrowed capital\n
    > Principal Repayment Condition:\n{self.principal_repayment_condition} principal must be returned by the end of the loan term.\n
    > Liquidation conditions:\n{self.liquidation_conditions}\n
    > Liquidator reward:\n{self.liquidator_reward} of the loan origination fee will be reserved for a liquidation bounty
    """


ILL001_TERMS = LoanTerm(
    "X7 Initial Liquidity Loan Term (001) - X7ILL001",
    0.5,
    5,
    "(4x leverage)",
    1,
    0,
    "1 Day",
    "28 Days",
    "25%",
    "No interest payment",
    "100%",
    "Failure of full repayment of principal by the end of the loan term will make the loan eligible for liquidation.",
    "5%",
)

ILL002_TERMS = LoanTerm(
    "X7 Initial Liquidity Loan Term (002) - X7ILL002",
    0.5,
    5,
    "(10x leverage)",
    4,
    4,
    "1 Day",
    "28 Days",
    "10%",
    "6.25%",
    "25% of the capital must be repaid on each quarter",
    "Failure to pay a premium + principal payment by its due date or repay the principal by the end of the loan term will make the loan eligible for liquidation.",
    "5%",
)

ILL003_TERMS = LoanTerm(
    "X7 Initial Liquidity Loan Term (003) - X7ILL003",
    0.5,
    5,
    "(6.66x leverage)",
    1,
    4,
    "1 Day",
    "7 Days",
    "15%",
    "6.25%",
    "100%",
    "Failure to pay a premium payment by its due date or repay the principal by the end of the loan term will make the loan eligible for liquidation.",
    "10%",
)
