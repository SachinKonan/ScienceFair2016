

"""

S = np.c_[x, x1]
plt.plot(S)
plt.show()

S += 0.2 * np.random.normal(size=S.shape)
S /= S.std(axis=0)


A = np.array([[1, 2], [1,2]])
X = np.dot(S, A.T)

ica = FastICA()
S_ = ica.fit_transform(X)  # Reconstruct signals
A_ = ica.mixing_  # Get estimated mixing matrix

pca = PCA()
H = pca.fit_transform(X)  # Reconstruct signals based on orthogonal components

###############################################################################
# Plot results

plt.figure()

models = [X, S, S_, H]
names = ['Observations (mixed signal)',
         'True Sources',
         'ICA recovered signals',
         'PCA recovered signals']
colors = ['red', 'steelblue', 'orange']

for ii, (model, name) in enumerate(zip(models, names), 1):
    plt.subplot(4, 1, ii)
    plt.title(name)
    for sig, color in zip(model.T, colors):
        plt.plot(sig, color=color)

plt.subplots_adjust(0.09, 0.04, 0.94, 0.94, 0.26, 0.46)
plt.show()

"""


if (len(x) == 2500):
    n = 4 * 2
    #fig, ax = plt.subplots(int(n / 2), n)
    overlap = 0.4

    nw = 250
    ns = int(nw * (1.0 - overlap))
    n0 = 0
    n1 = n0 + nw
    N = N

    counter = 0
    counter1 = 0
    counter2 = 1
    a = []

    while True:
        data = x[n0:n1]
        array = data * np.hanning(len(data))
        r = counter // n
        c = counter % n
        #ax[r][c].plot(array)
        n0 += ns
        n1 += ns
        counter += 2


        if(counter1 %2== 0):
            a = [array]

        else:
            a.append(array)
            if(counter1 == 1):

                data = np.array(a).T

                mixingMatrix = np.array([1,2])
                data = mixingMatrix * data

                ica = PCA()
                sources = ica.fit_transform(data)

                fig = plt.figure()
                ax = plt.subplot(111)
                ax.plot(sources,label = ' ICA')
                ax.legend()
                plt.show()

                break

                a = []
        counter1 += 1
        if n1 > N:
            break
else:
    print("Error your data vector is not the proper length")
