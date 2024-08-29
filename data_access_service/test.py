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
        timestamps, speed_data, timestamps_resampled, speed_data_resampled = data_access.get_rpm()

        # Check if data was retrieved successfully
        if timestamps is not None and speed_data is not None:
            logging.info(f"Successfully retrieved {len(speed_data)} speed records for user_id {user_id}.")

            # Create a Plotly line plot
            fig = go.Figure()

            # Plot resampled data (less dense)
            fig.add_trace(go.Scattergl(
                x=timestamps_resampled,
                y=speed_data_resampled,
                mode='lines+markers',
                marker=dict(size=3),
                line=dict(width=1),
                name='Speed (Resampled)'
            ))

            # Keep the original, dense data in a hidden trace for zooming
            fig.add_trace(go.Scattergl(
                x=timestamps,
                y=speed_data,
                mode='lines+markers',
                marker=dict(size=1),  # Smaller markers for detailed data
                line=dict(width=1),
                name='Speed (Full Data)',
                visible='legendonly'  # Hide by default, reveal on zoom
            ))

            fig.update_layout(
                title='Vehicle Speed Over Time',
                xaxis_title='Time',
                yaxis_title='Speed (km/h)',
                xaxis=dict(showspikes=True, spikecolor="green", spikethickness=1),
                yaxis=dict(showspikes=True, spikecolor="orange", spikethickness=1),
                hovermode="x unified",
                autosize=True
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
