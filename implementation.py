#
# implementation.py
#


import math
import numpy as np
import scipy.constants
import matplotlib.pyplot as plot


'''
Constants.
'''

PI = scipy.constants.pi
lightspeed = scipy.constants.c
electric_permittivity_vacuum = scipy.constants.epsilon_0
magnetic_permeability_vacuum = scipy.constants.mu_0


'''
Solve the linear system [Z][I]=[V] to find the currents along the z axis.
'''

def solve_dipole_antenna_mom(
        frequency,
        antenna_length,
        antenna_radius,
        segments_count,
        powered_segment
    ):

    '''
    Inferred parameters.
    '''

    angular_frequency = 2*PI*frequency

    wavelength = float(lightspeed)/frequency
    wavenumber = (2*PI)/wavelength

    half_base_width = float(antenna_length)/(segments_count+1)

    electric_permittivity = electric_permittivity_vacuum
    magnetic_permeability = magnetic_permeability_vacuum

    '''
    Auxiliary function.
    '''

    def phi(m, n):

        if m == n:

            a = (1.0/(2*PI*half_base_width))
            b = math.log(half_base_width/antenna_radius)
            c = a * b

            d = (1/(4*PI))
            e = complex(0, wavenumber)
            f = d * e

            return c - f

        else:

            z_m = (m*half_base_width) - (antenna_length/2)
            z_n = (n*half_base_width) - (antenna_length/2)

            a = math.pow((z_m - z_n), 2)
            b = math.pow(antenna_radius, 2)
            c = math.sqrt(a + b)

            d = complex(0, -(wavenumber*c))
            e = np.exp(d)

            f = 4*PI*c

            return e / f

    '''
    Initialize matrices.
    '''

    Z = np.zeros((segments_count, segments_count), dtype=complex)
    V = np.zeros((segments_count, 1), dtype=complex)

    '''
    Calculate the voltages column matrix (V).
    '''

    V[powered_segment-1][0] = complex(0, -(angular_frequency*electric_permittivity))

    '''
    Calculate the impedance matrix.
    '''

    for m in range(segments_count):

        for n in range(segments_count):

            a = phi((m-0.5), (n-0.5))
            b = phi((m-0.5), (n+0.5))
            c = phi((m+0.5), (n-0.5))
            d = phi((m+0.5), (n+0.5))

            k = math.pow(wavenumber, 2)
            A_mn = math.pow(half_base_width, 2) * phi(m, n)
            O_mn = a - b - c + d

            Z[m][n] = (k*A_mn) - O_mn

    '''
    Solve the linear system [Z][I]=[V] (find currents).
    '''

    I = np.linalg.solve(Z, V)

    return I
    
def momplot(wavelength,antenna_length,segments,):
    
    # wavelenth以m为单位
    # 天线长度以波长的倍数为单位
    
    
    frequency = float(lightspeed)/wavelength
    
    antenna_length = wavelength*antenna_length
    antenna_radius = wavelength*math.pow(10,-4)
    
    # 激励单元
    # Python中两个斜杠即双斜杠（//）表示地板除，即先做除法（/），
    #然后向下取整（floor）。至少有一方是float型时，结果为float型；两个数都是int型时，结果为int型。
    powered_segment = (segments//2)+1
    
    # 每一段的半宽
    #
    half_base_width = float(antenna_length)/(segments+1)

    # 计算电流分布
    I = solve_dipole_antenna_mom(frequency, antenna_length, antenna_radius, segments, powered_segment)
    
    # 馈电处的电流和阻抗
    I_in = I[powered_segment-1]
    Z_in = 1/I_in
    
    I_absolute = np.absolute(I)
    I_mV = [(i*1000) for i in I_absolute]
    I_mV = [0] + I_mV + [0]

    x_neg = [ ( ((n*half_base_width)-(antenna_length/2)) / wavelength)  for n in range((segments+2)//2)]
    x_pos = [-x for x in x_neg]
    x_rev = [x for x in reversed(x_pos)]
    x = x_neg + [0] + x_rev
    
    
    # print(I)
    # print(type(I[0][0]))
    #plot.figure()
    plot.plot(x, I_mV)
    plot.legend(["segments="+str(segments)], loc="upper right")
    plot.title("Current Distribution (L = λ/2)")
    plot.xlabel("Z/λ")
    plot.ylabel("|I| (mA)")
    plot.savefig("graphs/currents.png", bbox_inches="tight")
    

    
    # 略去所有En相同的相位，即所有常数，转置为1*n的矩阵，和In相乘
    # math中的cos不能处理numpy的array，numpy自带的cos可以处理
    theta = np.linspace(-PI, PI, 50000)
    wavenumber = (2*PI)/wavelength
    k = wavenumber*lightspeed
    li = complex(0,1)
    E = 0
    for n in range(segments):
        
        phase = np.exp(-li*k*(n-(segments-1)/2)*half_base_width*np.cos(theta))
        En = phase*np.sin(theta)*I[n][0]
        E = E+En
    fig, ax = plot.subplots()
    ax = plot.subplot(111, projection='polar')
    plot.plot(theta,np.abs(np.real(E))/max(np.abs(np.real(E))))
    plot.savefig("graphs/pattern.png", bbox_inches="tight")
    # print(abs(np.real(E)))
    
    '''
    sympy的远场的写法
    theta = sympy.symbols('theta')
    
    
    E = 0 
    for n in range(segments):
        
        phase = sympy.exp(-sympy.I*k*(n-(segments-1)/2)*half_base_width*sympy.cos(theta))
        En = phase*sympy.sin(theta)*I[n][0]
        E = E+En
    
    sympy.plot(sympy.Abs(E),(theta,-PI/2,PI/2))
    '''

# momplot(1,0.5,13)
    