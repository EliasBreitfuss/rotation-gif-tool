import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from io import BytesIO

st.title("Rotations-GIF Generator")

diameter = st.number_input("Kreisdurchmesser (cm)", min_value=1.0, value=28.0)
rpm = st.number_input("Umdrehungen pro Minute (U/min)", min_value=1.0, value=45.0)

if st.button("GIF generieren"):
    radius_m = diameter / 200
    angular_velocity = rpm * 2 * np.pi / 60
    tangential_velocity = angular_velocity * radius_m

    fig, ax = plt.subplots()
    ax.set_xlim(-radius_m * 1.2, radius_m * 1.2)
    ax.set_ylim(-radius_m * 1.2, radius_m * 1.2)
    ax.set_aspect('equal')
    ax.axis('off')
    circle = plt.Circle((0, 0), radius_m, fill=False)
    ax.add_patch(circle)
    point, = ax.plot([], [], 'ro', markersize=8)

    def update(frame):
        angle = 2 * np.pi * frame / 60
        x = radius_m * np.cos(angle)
        y = radius_m * np.sin(angle)
        point.set_data(x, y)
        return point,

    ani = animation.FuncAnimation(fig, update, frames=60, interval=1000/15, blit=True)
    buf = BytesIO()
    ani.save(buf, writer='pillow', format='gif')
    buf.seek(0)

    st.image(buf, caption=f"Tangentialgeschwindigkeit: {tangential_velocity:.2f} m/s")
    st.download_button("GIF herunterladen", buf, file_name="rotation.gif", mime="image/gif")
