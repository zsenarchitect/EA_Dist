
__title__ = "SlopeCalculator"
__doc__ = "This button does SlopeCalculator when left click"
import webbrowser


def slope_calculator():
    path = "https://rechneronline.de/slope/"
    webbrowser.open(path)

if __name__ == "__main__":
    slope_calculator()