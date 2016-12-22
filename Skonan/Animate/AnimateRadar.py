import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation


# First set up the figure, the axis, and the plot element we want to animate
fig = plt.figure()
ax = plt.axes(xlim=(0, 2), ylim=(-10,10))
plt.xlabel('Time')
plt.ylabel('Amplitude')
plt.title('Received Input')
line, = ax.plot([], [], lw=2)

#file1 = open('testRadar4ft.out','r')
#file2 = open('testTime4ft.out','r')

#radarData = []
#timeData = []


# initialization function: plot the background of each frame
def init():
    line.set_data([], [])
    return line,

# animation function.  This is called sequentially
def animate(i):
    x = np.linspace(0, 2, 1000)
    y = 5 * np.sin(2 * np.pi * (x - 0.01 * i)) + 3* np.sin(2 * np.pi * 0.3 * (x - 0.01 * i))
    line.set_data(x, y)
    return line,

# call the animator.  blit=True means only re-draw the parts that have changed.
if __name__ == '__main__':


    anim = animation.FuncAnimation(fig, animate,init_func=init,frames=100, interval=75, blit=True)

    # save the animation as an mp4.  This requires ffmpeg or mencoder to be
    # installed.  The extra_args ensure that the x264 codec is used, so that
    # the video can be embedded in html5.  You may need to adjust this for
    # your system: for more information, see
    # http://matplotlib.sourceforge.net/api/animation_api.html

    anim.save('Receive.mp4', fps=30)

    plt.show()