from modules.Data import Data
from modules.FeatureEngineering import FeatureEngineering



def main():
    data = Data()

    featureEngineering = FeatureEngineering(data)

    featureEngineering.apply_dv1()

    
    featureEngineering.apply_dv2()


if __name__ == "__main__":
    main()