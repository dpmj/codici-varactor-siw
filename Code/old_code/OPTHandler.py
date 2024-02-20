# import VNAHandler as VNA
import ERReval as ERR
import FILTHandler as FILT
# import s2pfile as s2p
##import TCPClient as TCP ##

"""
This Python code appears to implement a coordinate descent or algorithm. 
The algorithm iteratively explores different values for each dimension of the 
input state vector, updating one dimension at a time based on the current step 
size. The objective is to minimize a given error function (evaluated by the 
ERR.evalerror function) by adjusting the parameters represented by the state 
vector.

Here are some key characteristics of the optimization algorithm in the code:

    Coordinate Descent: The algorithm updates each dimension of the state vector
    independently in each iteration, keeping other dimensions fixed. This is 
    evident in the loop where each dimension of the provisional state (state_p) 
    is updated individually.

    Step Size Adjustment: The algorithm dynamically adjusts the step size (step)
    during the optimization process. The step size is initially set to step0 and
    is halved if progress is not made in reducing the error. Additionally, there
    is a check for the minimum step size (minstep) to avoid excessively small 
    steps.

    Exploration and Convergence Flags: The explored and converged lists are used
    as flags to track whether a dimension has been explored and whether it has 
    converged, respectively. These flags are updated based on the optimization 
    progress.

    Iteration Limit: The optimization is limited by the maximum number of 
    iterations (maxiter). If this limit is reached before convergence, the 
    algorithm terminates and returns a 'MAXITER' status.
"""



def Optimize (spi, state0, NPoints, mask, step0, maxiter, host, port):
    errortol=0.001  # Error máximo permitido? No deja configurarlo?
    minstep=(30/4096)  # Paso mínimo? En base a qué esos números?
    
    iteration=0
    dimension=len(state0)
    explored=[0]*dimension  # list of [0, 0, 0]
    converged=[0]*dimension
    
    state=state0                             #Best state, init in state0
    state_p=[0]*dimension                    #Provisional state, used to check
    

    coordinates = basemat(dimension)         #Coordinates base
    stepn=0                                  #Previous step
    step=step0                               #Scalar step    
    step_v=[x*step for x in coordinates[0]]  #Vectorial step
    
    #Measure filter in state0
    mat = FILT.measure(spi, state, NPoints, host, port)
##    TCP.querytest('CALC:DATA:SNP? 2', host, port)
##    TCP.querytest('CALC:DATA:SNP? 2', host, port)
##    TCP.querytest('CALC:DATA:SNP? 2', host, port)
##    TCP.querytest('CALC:DATA:SNP? 2', host, port)
##    s2p.mat2file(mat, 's2ptest', 'test')

    #Eval its error En
    En = ERR.evalerror(mat, mask)
    print('State0 total error: ' + str(En))

    while iteration<maxiter:
        iteration=iteration+1
        print(iteration, end=': ')
        print('Step = {:2.4f}'.format(step), end='. ')
        
        #Update exploration flag
        explored[0]=1
        
        #EVALUAR
        #Generate new state.
        # update state with step. Boundaries.
        print('State:', end=' ')
        for i in range(dimension):
            state_p[i]=state[i]+step_v[i]  # Apply step, getting new state (variable values)
            if state_p[i]<0:  #TO-DO boundaries as parameters
                state_p[i] = 0
            elif state_p[i]>12:
                state_p[i] = 12
                
            print('{:2.4f}'.format(state_p[i]), end=', ')

        # Measure filter in new state
        mat = FILT.measure(spi, state_p, NPoints, host, port)

                     
        #Eval its error E
        E = ERR.evalerror(mat, mask)
        print('Total Error = {:10.4f}'.format(E), end=' ')
        #input()

        # Compare new and old errors.
        if E<En:  # if we made progress (less error!)

            print('OK')
            #ASUMIR NUEVO PUNTO
            state=list(state_p)  # list inside list??
            
            #Actualizar error
            En=E  # old error updated with new error
            
            #Flag convergido (actualizado)
            converged[0]=1

            #SI E<errortol: SALIDA con SUPERADO
            if E<errortol:
                print ('Current state accomplishes conditions')
                return ['SOLVED', state, mat]

            #COMPARAR STEP
            if step==stepn:
                #MISMO STEP
                stepn=step  #Hace copia
            else:
                #STEP<MINIMO?
                if abs(step)<=minstep:
                    #CAMBIO DE PARAMETRO
                    #|STEP| = |STEP0|
                    stepn=0                    #Step anterior como si 0
                    coordinates.append(coordinates.pop(0))
                    step=step0
                    step_v=[x*step for x in coordinates[0]]

                    #Actualizar flag exploracion
                    explored.append(explored.pop(0))
                    
                    #Actualizar flag convergencia SI
                    converged.append(converged.pop(0))
                    converged[0]=1
                    print('Converged vector:', end=' ')
                    for i in range(dimension):
                        print(str(converged[i]), end=', ')

                    print('\n')
                    
                else:
                    #SI NO ES LA RACHA DE SALIDA, STEP/2
                    stepn=step
                    if abs(step) != step0:
                        step=step/2
                        step_v=[x*step for x in coordinates[0]]
                    
                    #ELSE STEP=

        else:
            print('NO')
            #COMPARAR STEP
            
            if abs(step) == abs(stepn): #|STEP|==|STEPN|
                #STEP<MINIMO?

                if abs(step) <= minstep:
                    #SI se ha estancado: SALIDA con OPTIMIZADO
                    if explored==[1]*dimension:
                        if converged[1:] == [0]*(dimension-1):
                            print ('Current state is already optimized')
                            return ['OPTIMIZED', state, mat]

                    #CAMBIO DE PARAMETRO
                    #|STEP| = |STEP0|
                    stepn=0                      #Step anterior como si 0
                    coordinates.append(coordinates.pop(0))
                    step=step0
                    step_v=[x*step for x in coordinates[0]]
                            
                    #Actualizar flag exploracion
                    explored.append(explored.pop(0))
                    #Actualizar flag convergencia NO
                    converged.append(converged.pop(0))
                    converged[0]=0
                    print('Converged vector:', end=' ')
                    for i in range(dimension):
                        print(str(converged[i]), end=', ')

                    print('\n')
                    
                else:
                    #STEP/2
                    stepn=step                   
                    step=step/2
                    step_v=[x*step for x in coordinates[0]]

            else:
                #STEP=-STEP
                stepn=step
                step=-step
                step_v=[x*step for x in coordinates[0]]

    print ('Maximun iterations reached')
    return ['MAXITER', state, mat]

def basemat(dimension):
    mat=[]
    for i in range(dimension):
        row=[0]*dimension
        row[i]=1
        mat.append(row)
        
    return mat
