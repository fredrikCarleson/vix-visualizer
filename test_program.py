#!/usr/bin/env python3
"""
Test script för VIX Visualizer
Kontrollerar att alla beroenden fungerar korrekt
"""

def test_imports():
    """Testa att alla nödvändiga paket kan importeras"""
    try:
        import yfinance as yf
        print("✅ yfinance - OK")
    except ImportError as e:
        print(f"❌ yfinance - FEL: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ pandas - OK")
    except ImportError as e:
        print(f"❌ pandas - FEL: {e}")
        return False
    
    try:
        import plotly.graph_objs as go
        print("✅ plotly - OK")
    except ImportError as e:
        print(f"❌ plotly - FEL: {e}")
        return False
    
    try:
        import webbrowser
        import os
        from datetime import datetime, timedelta
        print("✅ Standardbibliotek - OK")
    except ImportError as e:
        print(f"❌ Standardbibliotek - FEL: {e}")
        return False
    
    return True

def test_data_fetch():
    """Testa att data kan hämtas"""
    try:
        import yfinance as yf
        from datetime import datetime, timedelta
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)  # Bara 30 dagar för test
        
        print("\n📊 Testar datahämtning...")
        
        vix_ticker = yf.Ticker("^VIX")
        vix = vix_ticker.history(start=start_date, end=end_date)
        
        if not vix.empty:
            print(f"✅ VIX data hämtad: {len(vix)} datapunkter")
            print(f"   Senaste VIX: {vix['Close'].iloc[-1]:.2f}")
        else:
            print("❌ Kunde inte hämta VIX data")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ Datahämtning misslyckades: {e}")
        return False

def main():
    print("🧪 VIX Visualizer - Test Script")
    print("=" * 40)
    
    # Testa imports
    if not test_imports():
        print("\n❌ Import-test misslyckades!")
        return False
    
    # Testa datahämtning
    if not test_data_fetch():
        print("\n❌ Datahämtning-test misslyckades!")
        return False
    
    print("\n✅ Alla tester godkända!")
    print("🚀 VIX Visualizer är redo att användas!")
    return True

if __name__ == "__main__":
    main() 