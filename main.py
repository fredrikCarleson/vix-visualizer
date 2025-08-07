import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
import webbrowser
import os
from datetime import datetime, timedelta
import numpy as np

def calculate_moving_average(data, window=20):
    """Beräkna glidande medelvärde"""
    return data.rolling(window=window).mean()

def determine_trend(current, ma):
    """Bestäm trend baserat på nuvarande värde vs MA"""
    if current > ma * 1.02:  # 2% över MA
        return "↗️ Bullish"
    elif current < ma * 0.98:  # 2% under MA
        return "↘️ Bearish"
    else:
        return "→ Neutral"

def get_overall_trend(vix_trend, vvix_trend, skew_trend):
    """Bestäm övergripande trend baserat på alla signaler"""
    bullish_count = sum(1 for trend in [vix_trend, vvix_trend, skew_trend] if "Bullish" in trend)
    bearish_count = sum(1 for trend in [vix_trend, vvix_trend, skew_trend] if "Bearish" in trend)
    
    if bullish_count >= 2:
        return "↗️ Bullish", "Flera volatilitetsindex visar minskande rädsla"
    elif bearish_count >= 2:
        return "↘️ Bearish", "Flera volatilitetsindex visar ökande oro"
    else:
        return "→ Neutral", "Blandade signaler - avvakta klarare trendriktning"

def get_market_analysis(vix, vvix, skew):
    """Analysera marknadsläge"""
    if vix > 30:
        return "Hög marknadsrädsla", "Extrem volatilitet - försiktighet krävs"
    elif vix > 25:
        return "Måttlig oro", "Något förhöjd volatilitet"
    elif vix < 15:
        return "Låg volatilitet", "Marknaden verkar lugn"
    else:
        return "Normal aktivitet", "Standard marknadsförhållanden"

def calculate_risk_score(vix, vvix, skew):
    """Beräkna Risk Score"""
    score = 0
    warnings = []
    
    if vix > 25:
        score += 1
        warnings.append("VIX > 25")
    if vvix > 120:  # Uppdaterad enligt krav
        score += 1
        warnings.append("VVIX > 120")
    if skew > 150:  # Uppdaterad enligt krav
        score += 1
        warnings.append("SKEW > 150")
    
    return score, warnings

def get_combined_warning_analysis(vix, vvix, skew):
    """Analysera kombinerad varningssignal"""
    risk_score, warnings = calculate_risk_score(vix, vvix, skew)
    
    if risk_score == 3:
        return "🔴 STARK VARNINGSIGNAL", "Alla tre index över trösklar - hög risk för större marknadsrörelse"
    elif risk_score == 2:
        return "🟡 MÅTTLIG VARNING", "Två av tre index över trösklar - ökad försiktighet"
    elif risk_score == 1:
        return "🟢 LÄTT VARNING", "Ett index över tröskel - övervaka utveckling"
    else:
        return "✅ INGEN VARNING", "Alla index inom normala nivåer"

def create_risk_indicators(data, risk_score):
    """Skapa riskindikatorer för grafen - endast vid varningar"""
    risk_periods = []
    
    # Visa gula områden endast vid måttlig eller stark varning
    if risk_score >= 2:  # Måttlig eller stark varning
        # Identifiera perioder med hög risk (2+ signaler aktiva)
        for i in range(len(data)):
            signals = 0
            if data['VIX'].iloc[i] > data['VIX_MA'].iloc[i]:
                signals += 1
            if data['VVIX'].iloc[i] > data['VVIX_MA'].iloc[i]:
                signals += 1
            if data['SKEW'].iloc[i] > data['SKEW_MA'].iloc[i]:
                signals += 1
                
            if signals >= 2:
                risk_periods.append(data.index[i])
    
    return risk_periods

def get_hover_warnings(vix, vvix, skew, vix_ma, vvix_ma, skew_ma):
    """Hämta varningsmeddelanden och trendsignaler för hover-information"""
    warnings = []
    trend_signals = []
    
    # Varningssignaler
    if vix > 25:
        warnings.append('<span style="color: white;">⚠️ Hög volatilitet (VIX > 25)</span>')
    if vvix > 120:
        warnings.append('<span style="color: white;">⚠️ Hög osäkerhet kring volatilitet (VVIX > 120)</span>')
    if skew > 150:
        warnings.append('<span style="color: white;">⚠️ Marknaden oroar sig för extremrisk (SKEW > 150)</span>')
    
    # Trendsignaler
    if vix > vix_ma * 1.02:
        trend_signals.append('<span style="color: white;">VIX: Över MA (Bearish)</span>')
    elif vix < vix_ma * 0.98:
        trend_signals.append('<span style="color: white;">VIX: Under MA (Bullish)</span>')
        
    if vvix > vvix_ma * 1.02:
        trend_signals.append('<span style="color: white;">VVIX: Över MA (Bearish)</span>')
    elif vvix < vvix_ma * 0.98:
        trend_signals.append('<span style="color: white;">VVIX: Under MA (Bullish)</span>')
        
    if skew > skew_ma * 1.02:
        trend_signals.append('<span style="color: white;">SKEW: Över MA (Bearish)</span>')
    elif skew < skew_ma * 0.98:
        trend_signals.append('<span style="color: white;">SKEW: Under MA (Bullish)</span>')
    
    # Kombinera varningar och trendsignaler - endast om de finns
    result = []
    if warnings:
        result.append('<span style="color: #ff6b6b; font-weight: bold;">🚨 VARNINGSIGNALER AKTIVA:</span><br>' + "<br>".join(warnings))
    if trend_signals:
        result.append('<span style="color: #ffd93d; font-weight: bold;">🔶 TRENDSIGNAL AKTIV:</span><br>' + "<br>".join(trend_signals))
    
    return "<br><br>".join(result) if result else ""

def create_html_dashboard(data, latest, vix_trend, vvix_trend, skew_trend, overall_trend, 
                         trend_description, market_status, market_description, risk_warnings, 
                         risk_score, combined_warning, combined_description):
    """Skapa HTML dashboard med ren layout och en enda Y-axel"""
    
    # Skapa huvudgraf med en enda Y-axel
    fig = go.Figure()
    
    # VIX (modern ljusblå linje) - matchar "Glidande Medelvärden" infobox
    fig.add_trace(go.Scatter(
        x=data.index, y=data['VIX'], 
        mode='lines+markers', name='VIX',
        line=dict(color='#87CEEB', width=4, shape='spline'),  # Tjockare, mjukare linje
        marker=dict(size=6, line=dict(width=1, color='white'), symbol='circle'),
        hovertemplate='<b style="color: white;">%{x}</b><br>' +
                     '<b style="color: #87CEEB;">VIX:</b> <span style="color: white;">%{y:.2f}</span><br>' +
                     '<b style="color: #90EE90;">VVIX:</b> <span style="color: white;">%{customdata[0]:.2f}</span><br>' +
                     '<b style="color: #FFB347;">SKEW:</b> <span style="color: white;">%{customdata[1]:.2f}</span><br>' +
                     '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━<br>' +
                     '%{customdata[2]}<extra></extra>',
        customdata=list(zip(data['VVIX'], data['SKEW'], 
                           [get_hover_warnings(vix, vvix, skew, data['VIX_MA'].iloc[i], data['VVIX_MA'].iloc[i], data['SKEW_MA'].iloc[i]) for i, (vix, vvix, skew) in enumerate(zip(data['VIX'], data['VVIX'], data['SKEW']))]))
    ))
    
    # VVIX (modern ljusgrön linje) - matchar VVIX infobox
    fig.add_trace(go.Scatter(
        x=data.index, y=data['VVIX'], 
        mode='lines+markers', name='VVIX',
        line=dict(color='#90EE90', width=4, shape='spline'),  # Tjockare, mjukare linje
        marker=dict(size=6, line=dict(width=1, color='white'), symbol='circle'),
        hoverinfo='skip',
        showlegend=True
    ))
    
    # SKEW (modern ljusgul-orange linje) - matchar SKEW infobox
    fig.add_trace(go.Scatter(
        x=data.index, y=data['SKEW'], 
        mode='lines+markers', name='SKEW',
        line=dict(color='#FFB347', width=4, shape='spline'),  # Tjockare, mjukare linje
        marker=dict(size=6, line=dict(width=1, color='white'), symbol='circle'),
        hoverinfo='skip',
        showlegend=True
    ))
    
    # Lägg till referenslinjer endast för VIX
    fig.add_hline(y=30, line_dash="dash", line_color="red", 
                 annotation_text="VIX Högrisk (30)")
    fig.add_hline(y=15, line_dash="dash", line_color="green", 
                 annotation_text="VIX Lågrisk (15)")
    
    # Lägg till riskindikatorer (gula områden) - endast vid varningar
    risk_periods = create_risk_indicators(data, risk_score)
    if risk_periods:
        for period in risk_periods:
            fig.add_vrect(
                x0=period, x1=period + timedelta(days=1),
                fillcolor="yellow", opacity=0.3,
                layer="below", line_width=0
            )
    
    # Uppdatera layout för grafen med modern design
    fig.update_layout(
        title="",
        height=500,
        showlegend=True,
        template="plotly_white",
        hovermode='x unified',
        plot_bgcolor='rgba(248, 250, 252, 0.8)',  # Subtilt gradient
        paper_bgcolor='white',
        font=dict(color='#1a202c', family='Inter, system-ui, sans-serif', size=12),
        margin=dict(l=50, r=50, t=30, b=50),
        
        # Modern Y-axel
        yaxis=dict(
            title="Indexvärde",
            side="left",
            gridcolor='rgba(226, 232, 240, 0.6)',  # Mjukare grid
            zeroline=False,
            range=[0, None],  # Börja på 0
            showline=True,
            linecolor='rgba(226, 232, 240, 0.8)',
            linewidth=1
        ),
        
        # Modern X-axel
        xaxis=dict(
            gridcolor='rgba(226, 232, 240, 0.6)',  # Mjukare grid
            showline=True,
            linecolor='rgba(226, 232, 240, 0.8)',
            linewidth=1
        ),
        
        # Modern hover-label
        hoverlabel=dict(
            bgcolor="rgba(45, 55, 72, 0.95)",
            bordercolor="rgba(74, 85, 104, 0.8)",
            font_size=12,
            font_family="Inter, system-ui, sans-serif",
            font_color="white"
        )
    )
    
    fig.update_xaxes(title_text="Datum")
    
    # Konvertera grafen till HTML
    graph_html = fig.to_html(include_plotlyjs='cdn', full_html=False)
    
    # Skapa HTML dashboard
    html_content = f"""
    <!DOCTYPE html>
    <html lang="sv">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>VIX Dashboard</title>
        <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
                 <style>
             body {{
                 background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                 font-family: 'Inter', system-ui, -apple-system, sans-serif;
                 color: #1a202c;
             }}
             .dashboard-container {{
                 max-width: 1400px;
                 margin: 0 auto;
                 padding: 20px;
             }}
             .header {{
                 background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                 color: white;
                 padding: 25px;
                 border-radius: 16px;
                 margin-bottom: 25px;
                 text-align: center;
                 box-shadow: 0 10px 25px rgba(102, 126, 234, 0.3);
                 backdrop-filter: blur(10px);
             }}
             .metrics-card {{
                 background: rgba(255, 255, 255, 0.95);
                 border-radius: 16px;
                 padding: 25px;
                 margin-bottom: 25px;
                 box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
                 backdrop-filter: blur(10px);
                 border: 1px solid rgba(255, 255, 255, 0.2);
             }}
                         .metric-item {{
                 display: flex;
                 justify-content: space-between;
                 align-items: center;
                 padding: 12px 0;
                 border-bottom: 1px solid rgba(226, 232, 240, 0.6);
                 transition: all 0.2s ease;
             }}
             .metric-item:hover {{
                 background: rgba(248, 250, 252, 0.5);
                 border-radius: 8px;
                 padding: 12px 8px;
                 margin: 0 -8px;
             }}
             .metric-item:last-child {{
                 border-bottom: none;
             }}
             .metric-label {{
                 font-weight: 600;
                 color: #2d3748;
                 font-size: 14px;
             }}
             .metric-value {{
                 color: #4a5568;
                 font-size: 14px;
             }}
             .trend-bullish {{
                 color: #38a169;
                 font-weight: 600;
             }}
             .trend-bearish {{
                 color: #e53e3e;
                 font-weight: 600;
             }}
             .trend-neutral {{
                 color: #718096;
                 font-weight: 600;
             }}
             .analysis-section {{
                 background: rgba(255, 255, 255, 0.95);
                 border-radius: 16px;
                 padding: 25px;
                 margin-bottom: 25px;
                 box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
                 backdrop-filter: blur(10px);
                 border: 1px solid rgba(255, 255, 255, 0.2);
             }}
             .warning-section {{
                 background: rgba(255, 243, 205, 0.9);
                 border: 1px solid rgba(255, 234, 167, 0.8);
                 border-radius: 16px;
                 padding: 20px;
                 margin-bottom: 25px;
                 backdrop-filter: blur(10px);
             }}
             .chart-container {{
                 background: rgba(255, 255, 255, 0.95);
                 border-radius: 16px;
                 padding: 25px;
                 box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
                 backdrop-filter: blur(10px);
                 border: 1px solid rgba(255, 255, 255, 0.2);
             }}
                         .info-box {{
                 background: rgba(227, 242, 253, 0.9);
                 border-left: 4px solid #2196f3;
                 padding: 20px;
                 margin: 15px 0;
                 border-radius: 12px;
                 backdrop-filter: blur(10px);
                 transition: all 0.2s ease;
                 box-shadow: 0 4px 16px rgba(33, 150, 243, 0.1);
             }}
             .info-box:hover {{
                 transform: translateY(-2px);
                 box-shadow: 0 8px 25px rgba(33, 150, 243, 0.15);
             }}
             .risk-high {{
                 background: rgba(255, 235, 238, 0.9);
                 border-left: 4px solid #f44336;
                 box-shadow: 0 4px 16px rgba(244, 67, 54, 0.1);
             }}
             .risk-high:hover {{
                 box-shadow: 0 8px 25px rgba(244, 67, 54, 0.15);
             }}
             .risk-medium {{
                 background: rgba(255, 243, 224, 0.9);
                 border-left: 4px solid #ff9800;
                 box-shadow: 0 4px 16px rgba(255, 152, 0, 0.1);
             }}
             .risk-medium:hover {{
                 box-shadow: 0 8px 25px rgba(255, 152, 0, 0.15);
             }}
             .risk-low {{
                 background: rgba(232, 245, 232, 0.9);
                 border-left: 4px solid #4caf50;
                 box-shadow: 0 4px 16px rgba(76, 175, 80, 0.1);
             }}
             .risk-low:hover {{
                 box-shadow: 0 8px 25px rgba(76, 175, 80, 0.15);
             }}
        </style>
    </head>
    <body>
        <div class="dashboard-container">
            <!-- Header -->
            <div class="header">
                <h1>📈 Volatility Dashboard</h1>
                <p class="mb-0">Realtidsanalys av VIX, VVIX och SKEW</p>
            </div>
            
            <!-- Metrics Card -->
            <div class="metrics-card">
                <h4 class="mb-3">📊 Aktuella Värden</h4>
                <div class="metric-item">
                    <span class="metric-label">VIX:</span>
                    <span class="metric-value">{latest['VIX']:.2f} | MA: {latest['VIX_MA']:.2f} | 
                    <span class="{'trend-bullish' if 'Bullish' in vix_trend else 'trend-bearish' if 'Bearish' in vix_trend else 'trend-neutral'}">{vix_trend}</span></span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">VVIX:</span>
                    <span class="metric-value">{latest['VVIX']:.2f} | MA: {latest['VVIX_MA']:.2f} | 
                    <span class="{'trend-bullish' if 'Bullish' in vvix_trend else 'trend-bearish' if 'Bearish' in vvix_trend else 'trend-neutral'}">{vvix_trend}</span></span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">SKEW:</span>
                    <span class="metric-value">{latest['SKEW']:.2f} | MA: {latest['SKEW_MA']:.2f} | 
                    <span class="{'trend-bullish' if 'Bullish' in skew_trend else 'trend-bearish' if 'Bearish' in skew_trend else 'trend-neutral'}">{skew_trend}</span></span>
                </div>
                <div class="metric-item">
                    <span class="metric-label">Övergripande Trend:</span>
                    <span class="metric-value">
                    <span class="{'trend-bullish' if 'Bullish' in overall_trend else 'trend-bearish' if 'Bearish' in overall_trend else 'trend-neutral'}">{overall_trend}</span> | {trend_description}</span>
                </div>
            </div>
            
            <!-- Risk Score Analysis -->
            <div class="analysis-section">
                <h4 class="mb-3">🎯 Risk Score Analysis</h4>
                <div class="row">
                    <div class="col-md-6">
                        <div class="info-box {'risk-high' if risk_score >= 2 else 'risk-medium' if risk_score == 1 else 'risk-low'}">
                            <h6>Risk Score: {risk_score}/3</h6>
                            <strong>Kombinerad Varning:</strong> {combined_warning}<br>
                            <strong>Beskrivning:</strong> {combined_description}<br><br>
                            <strong>Formel:</strong> (VIX > 25 → +1) + (VVIX > 120 → +1) + (SKEW > 150 → +1)
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="info-box">
                            <h6>📊 Aktuella Värden vs Trösklar</h6>
                            <strong>VIX:</strong> {latest['VIX']:.2f} (Tröskel: 25) {'✅' if latest['VIX'] <= 25 else '⚠️'}<br>
                            <strong>VVIX:</strong> {latest['VVIX']:.2f} (Tröskel: 120) {'✅' if latest['VVIX'] <= 120 else '⚠️'}<br>
                            <strong>SKEW:</strong> {latest['SKEW']:.2f} (Tröskel: 150) {'✅' if latest['SKEW'] <= 150 else '⚠️'}
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Market Analysis -->
            <div class="analysis-section">
                <h4 class="mb-3">🔍 Marknadsanalys</h4>
                <div class="info-box">
                    <strong>Marknadsstatus:</strong> {market_status}<br>
                    <strong>Beskrivning:</strong> {market_description}
                </div>
            </div>
            
            <!-- Risk Warnings -->
            {f'''
            <div class="warning-section">
                <h5 class="mb-2">⚠️ Aktiva Riskvarningar</h5>
                {''.join([f'<div class="mb-1">• {warning}</div>' for warning in risk_warnings])}
            </div>
            ''' if risk_warnings else ''}
            
            <!-- Chart -->
            <div class="chart-container">
                <h4 class="mb-3">�� Volatility Indices - Trendanalys med Riskindikatorer</h4>
                                 <div class="info-box">
                     <strong>📊 Grafstruktur:</strong> En enda Y-axel för alla index (VIX lågt, VVIX/SKEW högt)<br>
                     <strong>Gula områden:</strong> Endast vid måttlig eller stark varningssignal<br>
                     <strong>Röd streckad linje:</strong> VIX över 30 = Extrem volatilitet<br>
                     <strong>Grön streckad linje:</strong> VIX under 15 = Låg volatilitet<br>
                     <strong>Hover-information:</strong> Visar alla indexvärden, varningssignaler och trendsignaler med tydlig separator
                 </div>
                {graph_html}
            </div>
            
            <!-- Interpretation Guide -->
            <div class="analysis-section">
                <h4 class="mb-3">📋 Tolkningsguide</h4>
                
                <div class="row">
                                         <div class="col-md-6">
                                                  <div class="info-box">
                              <h6>VIX - Volatility Index</h6>
                              <strong>Risk nivå:</strong> Måttlig Risk<br>
                              <strong>Vad det mäter:</strong> Implied volatilitet (30 dagar) på S&P 500<br>
                              <strong>Tolkning vid höga nivåer:</strong> Förväntad hög volatilitet – ofta vid oro<br>
                              <strong>Normalt intervall:</strong> 12-20 | <strong>Varningsnivå:</strong> Över 25-30
                          </div>
                     </div>
                    <div class="col-md-6">
                                                 <div class="info-box risk-low">
                             <h6>VVIX - Volatility of VIX</h6>
                             <strong>Risk nivå:</strong> Låg Risk<br>
                             <strong>Vad det mäter:</strong> Volatilitet i VIX-indexet<br>
                             <strong>Tolkning vid höga nivåer:</strong> Osäkerhet i osäkerheten – stressnivå<br>
                             <strong>Normalt intervall:</strong> 80-100 | <strong>Varningsnivå:</strong> Över 110-120
                         </div>
                    </div>
                </div>
                
                <div class="row mt-3">
                    <div class="col-md-6">
                                                 <div class="info-box risk-medium">
                             <h6>SKEW - Tail Risk Index</h6>
                             <strong>Risk nivå:</strong> Måttlig Risk<br>
                             <strong>Vad det mäter:</strong> Marknadens sannolikhet för extrem nedgång<br>
                             <strong>Tolkning vid höga nivåer:</strong> Efterfrågan på långt utanför pengarna-putar ökar<br>
                             <strong>Normalt intervall:</strong> 110-130 | <strong>Varningsnivå:</strong> Över 145-150
                         </div>
                    </div>
                    <div class="col-md-6">
                        <div class="info-box">
                            <h6>Glidande Medelvärden</h6>
                            <strong>Bullish signal:</strong> När volatilitetsindex faller under sitt MA - minskande rädsla<br>
                            <strong>Bearish signal:</strong> När volatilitetsindex stiger över sitt MA - ökande oro
                        </div>
                    </div>
                </div>
            </div>
            
            <!-- Footer -->
            <div class="text-center text-muted mt-4">
                <small>Data uppdaterad: {datetime.now().strftime('%Y-%m-%d %H:%M')} | 
                Kör programmet igen för att uppdatera data</small>
            </div>
        </div>
        
        <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    </body>
    </html>
    """
    
    return html_content

def main():
    print("🚀 Startar VIX Visualizer Dashboard...")
    
    # 📅 Beräkna datum för senaste 6 månaderna
    end_date = datetime.now()
    start_date = end_date - timedelta(days=180)
    
    print(f"📅 Hämtar data från {start_date.strftime('%Y-%m-%d')} till {end_date.strftime('%Y-%m-%d')}")
    
    try:
        # 📈 Ladda ner data
        print("📊 Hämtar VIX data...")
        vix_ticker = yf.Ticker("^VIX")
        vix = vix_ticker.history(start=start_date, end=end_date)["Close"].rename("VIX")
        print(f"VIX data: {len(vix)} datapunkter")
        
        print("📊 Hämtar VVIX data...")
        vvix_ticker = yf.Ticker("^VVIX")
        vvix = vvix_ticker.history(start=start_date, end=end_date)["Close"].rename("VVIX")
        print(f"VVIX data: {len(vvix)} datapunkter")
        
        print("📊 Hämtar SKEW data...")
        skew_ticker = yf.Ticker("^SKEW")
        skew = skew_ticker.history(start=start_date, end=end_date)["Close"].rename("SKEW")
        print(f"SKEW data: {len(skew)} datapunkter")
        
        # 🔗 Slå ihop till en enda DataFrame med outer join
        print("🔗 Kombinerar data...")
        data = pd.concat([vix, vvix, skew], axis=1, join='outer')
        
        # Ta bort rader där alla värden är NaN
        data = data.dropna(how='all')
        
        # Fyll i saknade värden med forward fill (senaste kända värde)
        data = data.ffill()
        
        # Ta bort rader där vi fortfarande har NaN-värden
        data = data.dropna()
        
        if data.empty:
            print("❌ Kunde inte hämta data. Kontrollera internetanslutning.")
            print("💡 Prova att köra programmet igen om några minuter.")
            return
            
        print(f"✅ Data hämtad! {len(data)} datapunkter")
        print(f"📅 Datumintervall: {data.index[0].strftime('%Y-%m-%d')} till {data.index[-1].strftime('%Y-%m-%d')}")
        
        # 🧮 Beräkna glidande medelvärden och analyser
        data['VIX_MA'] = calculate_moving_average(data['VIX'])
        data['VVIX_MA'] = calculate_moving_average(data['VVIX'])
        data['SKEW_MA'] = calculate_moving_average(data['SKEW'])
        
        # 📊 Hämta senaste värden
        latest = data.iloc[-1]
        latest_date = data.index[-1].strftime('%Y-%m-%d')
        
        # 🔍 Beräkna trender
        vix_trend = determine_trend(latest['VIX'], latest['VIX_MA'])
        vvix_trend = determine_trend(latest['VVIX'], latest['VVIX_MA'])
        skew_trend = determine_trend(latest['SKEW'], latest['SKEW_MA'])
        
        overall_trend, trend_description = get_overall_trend(vix_trend, vvix_trend, skew_trend)
        market_status, market_description = get_market_analysis(latest['VIX'], latest['VVIX'], latest['SKEW'])
        
        # 🔍 Risk Score Analysis 
        risk_score, risk_warnings = calculate_risk_score(latest['VIX'], latest['VVIX'], latest['SKEW'])
        combined_warning, combined_description = get_combined_warning_analysis(latest['VIX'], latest['VVIX'], latest['SKEW'])
        
        # ⚠️ Riskvarningar med uppdaterade trösklar
        risk_warnings_formatted = []
        if latest['VIX'] > 25:
            risk_warnings_formatted.append("⚠️ Hög volatilitet (VIX > 25)")
        if latest['VVIX'] > 120:
            risk_warnings_formatted.append("⚠️ Hög osäkerhet kring volatilitet (VVIX > 120)")
        if latest['SKEW'] > 150:
            risk_warnings_formatted.append("⚠️ Marknaden oroar sig för extremrisk (SKEW > 150)")
        
        # 📈 Skapa HTML dashboard
        print("\n📊 Skapar professionell dashboard...")
        
        html_content = create_html_dashboard(
            data, latest, vix_trend, vvix_trend, skew_trend, 
            overall_trend, trend_description, market_status, 
            market_description, risk_warnings_formatted, risk_score, combined_warning, combined_description
        )
        
        # 💾 Spara som HTML och öppna i webbläsare
        html_file = "vix_dashboard.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"💾 Dashboard sparad som: {html_file}")
        print("🌐 Öppnar i webbläsare...")
        
        # Öppna i webbläsare
        webbrowser.open('file://' + os.path.realpath(html_file))
        
        # Skriv ut sammanfattning
        print(f"\n📊 SENASTE VÄRDEN ({latest_date}):")
        print(f"VIX: {latest['VIX']:.2f} (MA: {latest['VIX_MA']:.2f}) - {vix_trend}")
        print(f"VVIX: {latest['VVIX']:.2f} (MA: {latest['VVIX_MA']:.2f}) - {vvix_trend}")
        print(f"SKEW: {latest['SKEW']:.2f} (MA: {latest['SKEW_MA']:.2f}) - {skew_trend}")
        print(f"\n🔍 ÖVERGIPANDE TREND: {overall_trend}")
        print(f"📈 MARKNADSSTATUS: {market_status}")
        
        print(f"\n🎯 RISK SCORE ANALYSIS:")
        print(f"Risk Score: {risk_score}/3")
        print(f"Kombinerad Varning: {combined_warning}")
        print(f"Beskrivning: {combined_description}")
        
        if risk_warnings_formatted:
            print("\n⚠️ AKTIVA RISKVARNINGAR:")
            for warning in risk_warnings_formatted:
                print(f"   {warning}")
        else:
            print("\n✅ Inga aktiva riskvarningar")
        
        print("\n✅ VIX Dashboard klar!")
        print("📊 Den professionella analysen visar marknadens nuvarande risknivåer och trender.")
        print("🔄 Kör programmet igen för att uppdatera data.")
        
    except Exception as e:
        print(f"❌ Ett fel uppstod: {str(e)}")
        print("🔧 Kontrollera internetanslutning och försök igen.")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()