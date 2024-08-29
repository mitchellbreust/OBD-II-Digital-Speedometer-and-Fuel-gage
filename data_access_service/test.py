import logging
import plotly.graph_objs as go
from data_access import DataAccess

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        # Initialize the DataAccess class with a sample user_id (e.g., 1)
        user_id = 1
        data_access = DataAccess(user_id=user_id)

        # Fetch speed data
        timestamps, speed_data = data_access.get_rpm()

        # Check if data was retrieved successfully
        if timestamps is not None and speed_data is not None:
            logging.info(f"Successfully retrieved {len(speed_data)} speed records for user_id {user_id}.")

            # Create a Plotly line plot
            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=timestamps,
                y=speed_data,
                mode='lines+markers',
                name='Speed'
            ))

            fig.update_layout(
                title='Vehicle coolant Over Time',
                xaxis_title='Time',
                yaxis_title='Coolant temp'
            )

            # Show the plot
            fig.show()
        else:
            logging.warning(f"No speed data found for user_id {user_id}.")

    except Exception as e:
        logging.error(f"An error occurred during data retrieval: {e}")
    
    finally:
        # Close the database connection
        data_access.close_data_access()

if __name__ == "__main__":
    main()
