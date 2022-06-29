from brownie import FundMe, MockV3Aggregator, network, config
from scripts.libraries import deploy_mocks, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS

def deploy_fund_me():
        account = get_account()

        # pass the price feed address to our fundme contract
        # If we are on rinkeby, use the associated address otherwise deploy mocks
        if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
            print("No Mocks deployed by Lee!")
            print(f"Network Name: {network.show_active()}")
            
            price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]
        # Get mocks from MockV3Aggregator.sol from contracts/test/ - This is from chainlink-mix repo 
        else: 
            print("Deploying Mocks by Lee!")
            deploy_mocks()
            price_feed_address = MockV3Aggregator[-1].address
            

        # Deploy fundme application
        fund_me = FundMe.deploy(
            price_feed_address,
            {"from": account}, 
            publish_source=config["networks"][network.show_active()].get("verify")
        )

        # One does print(f"") when parameters are being passed 
        print(f"Contract deploy to {fund_me.address}")
        return fund_me

def main():
        deploy_fund_me()