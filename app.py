from flask import Flask, render_template
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Use a non-interactive backend
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    # Load the portfolio data
    df = pd.read_excel('portfolio_data.xlsx')
    
    # Calculate the performance (as a percentage of gain/loss)
    df['Performance'] = ((df['Current Price'] - df['Purchase Price']) / df['Purchase Price'] * 100).round(2)
    
    # Calculate the annual dividend for each stock
    df['Annual Dividend'] = df['Shares'] * df['Current Price'] * (df['Dividend Yield (%)'] / 100)

    # Calculate the total value of the portfolio
    total_value = (df['Current Price'] * df['Shares']).sum()

    # Calculate the total annual dividend from all stocks
    total_annual_dividend = df['Annual Dividend'].sum()

    # Create the pie chart
    create_pie_chart(df)

    # Convert DataFrame to a list of dictionaries for rendering
    data = df.to_dict(orient='records')

    # Return the rendered template with portfolio data and total dividend
    return render_template('index.html', data=data, total_annual_dividend=total_annual_dividend)

def create_pie_chart(df):
    # Set the figure size for the pie chart
    plt.figure(figsize=(8, 6))

    # Calculate asset allocation based on current values (Shares * Current Price)
    plt.pie(df['Shares'] * df['Current Price'], labels=df['Stock'], autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures the pie chart is circular.

    # Save the pie chart as an image in the static folder
    plt.savefig('static/pie_chart.png')
    plt.close()  # Close the figure to free up memory

if __name__ == '__main__':
    app.run(debug=True)
