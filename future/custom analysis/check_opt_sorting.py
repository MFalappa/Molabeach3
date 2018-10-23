# -*- coding: utf-8 -*-
""""
Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

Copyright (C) 2017 FONDAZIONE ISTITUTO ITALIANO DI TECNOLOGIA
                   E. Balzani, M. Falappa - All rights reserved

@author: edoardo.balzani87@gmail.com; mfalappa@outlook.it

                                Publication:
         An approach to monitoring home-cage behavior in mice that 
                          facilitates data sharing
                          
        DOI: 10.1038/nprot.2018.031      

*******************************************************************************
THIS SCRIP ISN'T DESCRIBED IN THE PAPER. IT WAS WRITTEN FOR OUR CUSTOM ANALYSIS
WE WILL INTRODUCE IN THE NEXT RELEASE OF PHENOPY AFTER A HARD DEBUG AND 
GENERALIZATION
*******************************************************************************

"""

import numpy as np
import sklearn.cluster as clust
from copy import deepcopy
from scipy.linalg import sqrtm
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.decomposition import PCA
import matplotlib.pylab as plt
import scipy.stats as sts
from scipy.cluster.vq import whiten
import pandas as pd
from sklearn.mixture import GaussianMixture
from time import clock


plt.close('all')

plt.ion()
 

def get_Sb_Sw(X,origL):
    """
        X = n x m matrix: n = num samples, m = num features
    """
    labels = np.unique(origL)
    nclass = labels.shape[0]
    Sb = np.zeros((X.shape[1], X.shape[1]))
    muk = np.zeros((nclass,X.shape[1]))
    nk = np.zeros(nclass)
    ###
    # INSERT NEW OVERALL MEAN
    ###
    ovrl_mean = np.nanmean(X,axis=0)
    for k in range(nclass):
        muk[k] = np.nanmean(X[origL==labels[k],:],axis=0)
        nk[k] = np.sum(origL == labels[k])
        v = (muk[k] - ovrl_mean).reshape((X.shape[1],1))
        Sb += nk[k]*np.dot(v,v.T)
    
    Sw = np.zeros((X.shape[1], X.shape[1]))
    for k in xrange(nclass):
        V = (X[origL == labels[k],:]-muk[k]).T
        Sw += np.dot(V,V.T)
    return Sb,Sw

def traceComp(W,Sb,Sw):
    Num = np.matrix.trace(np.dot(np.dot(W.T,Sb),W))
    Den = np.matrix.trace(np.dot(np.dot(W.T,Sw),W))
    return np.array(Num, dtype=float) / Den

def lda_km(X,K,d,W0,imax,niter_Kmeans=10):
    """
        X : n x m matrix, n spikes, m waveform sample
        K : number of clusters
        d : subspace dim (d<K)
        W0 : m x d projection matrix
        imax : iteretion max
    """
    W = W0
    weight_means = 0
    L1 = np.random.choice(range(K),size=(X.shape[0],))
    L =  np.ones(X.shape[0])
    i = 0
    while i < imax and (i == 0 or np.sum(L != L1) > 0):
#        print 'Iteration num:',i
        Y = np.dot(X,W)
        if Y.shape[0] is 1:
            Y = whiten(Y)
        L = deepcopy(L1)
#        if i>0:
#            Sb,Sw = get_Sb_Sw(X,L1)
#            print 'pre Kmeans', traceComp(W,Sb,Sw)
        score = -np.inf
        for k in xrange(niter_Kmeans):
            kmeans = clust.KMeans(n_clusters=K)
            kmeans = kmeans.fit(Y)
            tmpscore = kmeans.score(Y)
            if tmpscore > score:  
                score = tmpscore
                L1 = kmeans.labels_
        lda = LinearDiscriminantAnalysis(solver="svd", store_covariance=True)
        try:
            lda = lda.fit(X,L1)
        except ZeroDivisionError:
            print 'ZeroDivisionError, too few wf in LDA-KM?'
            break
            
        W = lda.scalings_ / np.linalg.norm(lda.scalings_,axis=0)

        
        weight_means = lda.xbar_
        i += 1

    return L1,W,weight_means,lda

def W0_init(X,K,d,imax,R,niter_Kmeans=10):
    index = range(X.shape[0])
    ratio_vect = np.zeros(imax)
    W_vect = []
    if R > len(index):
        R = len(index)
    for i in xrange(imax):
#        print 'W0 iteration %d'%i
        choice = np.random.choice(index,R,False)
        if i%2 == 0:
            W0 = np.random.rand(X.shape[1],d)
        else:
            pca = PCA()
            pca = pca.fit(X[choice,:])
            W0 = pca.components_[:d,:].T
#            pca.transform
        L,W,weight_means,lda = lda_km(X,K,d,W0,imax=imax,niter_Kmeans=niter_Kmeans)
        W_vect += [W]
        Sb,Sw = get_Sb_Sw(X,L)
        ratio_vect[i] = traceComp(W,Sb,Sw)
    i = np.argmax(ratio_vect)
    return W_vect[i]

def excludeSmallerClass(L,mdl=None, Y=None, X=None):
    labels = np.unique(L)
    smaller = L.shape[0]
    for l in labels:
        nclass = np.sum(L==l)
        if nclass < smaller:
            smaller = nclass
            sml_lab = l
    return sml_lab

def excludeLargerVarianceClass(L, mdl=None ,Y=None,X=None):
    prod_eig = np.zeros(mdl.covariances_.shape[0])
    for k in xrange(mdl.covariances_.shape[0]):
        if mdl.covariances_[k].shape[0] > 1:
            prod_eig[k] = np.linalg.det(mdl.covariances_[k])
        else:
            prod_eig[k] = np.abs(mdl.covariances_[k][0])
    return np.nanargmax(prod_eig)
    
def excludeMaxDistFromCentroids(L, mdl=None, Y=None, X=None):
    try:
        max_dist = np.zeros(mdl.covariances_.shape[0])
    except:
        max_dist = np.zeros(mdl.means_.shape[0])
    for k in np.unique(L):
        max_dist[k] = np.nanmean(np.linalg.norm(Y[L==k,:]-np.nanmean(Y[L==k,:],axis=0),axis=1))
    return np.nanargmax(max_dist)

def excludeFirstCluster(L, mdl=None, Y=None, X=None):
    return 0

def excludeNoisyWf(L, mdl=None, Y=None, X=None):
    labels = np.unique(L)
    corr_list = np.zeros(labels.shape[0])
    for l in labels:
        s = np.nanstd(X[L==l,:], axis=0)
        try:
            corr_list[l], _ = sts.pearsonr(s[:-1],s[1:])
        except IndexError:
            pass
    return np.argmin(corr_list)
    
def GMM_LDA(X,L1,d,W0,imax,niter_Kmeans=10,outlierW=0.01,tol=10**-4,excludeFun=excludeFirstCluster,noise_p = 0.1):
    W = W0
    i = 0
    labels = np.unique(L1)
    K = len(labels)
    # WEIGHT TO HAVE A SMALL PRIOR FOR NOISE
    weights = np.zeros(K+1)
    weights[0] = noise_p
    weights[1:] = (1-noise_p) / (K)
    
    i = 0
    vold = np.inf
    v = 0
    while i < imax and np.abs(v-vold) >= tol:
        vold = v
        Y = np.dot(X, W)
        
        Y = whiten(Y)
            
            
            
        mdl = GaussianMixture(n_components=K+1,weights_init=weights)
        # NO PRIOR WEIGHTS AFTER FIRST ITER
        weights = None
        mdl.fit(Y)
        L = mdl.predict(Y)
        
        # exclude noise using a criteria specified as input
        if np.unique(L).shape[0] == K + 1:
            noise_lab = excludeFun(L, mdl = mdl, Y = Y, X = X)
            outFreeL = L[L != noise_lab]
            outFreeX = X[L != noise_lab,:]
        else:
            noise_lab = np.nan
            outFreeX = X
            outFreeL = L
        lda = LinearDiscriminantAnalysis(solver="svd", store_covariance=True)
        try:
            lda = lda.fit(outFreeX,outFreeL)
        except ZeroDivisionError:
            print 'Zero Division, too many outliers?'
            break
            
        W = lda.scalings_ / np.linalg.norm(lda.scalings_,axis=0)
        # TEST OUTLIER FREE
        Sb,Sw = get_Sb_Sw(outFreeX,outFreeL)

        v = traceComp(W,Sb,Sw)
        if np.isnan(v):
            pass
#        print 'iter %d \t  v: %f'%(i,v)
        i += 1
    wfInd = L != noise_lab
    outFreeY = Y[wfInd,:]
    
    return mdl,Y,weights, outFreeY, wfInd

def selectK(X,d,Widxmax,KMidxmax,GMMidxmax,R,niter_Kmeans=10,tol=10**-4,excludeFun=excludeSmallerClass, Klim=4, noise_p = 0.05):
    # for k equals to 1 simply GMM of raw waveforms, detect noise and saves labels
    L_dict = {}
    Y_dict = {}

    
    K = 1
    K1 = 1
    
    while K1 == K and K < Klim:
        K += 1
        K1 += 1
        try:
            W = W0_init(X,K,d,Widxmax,R,niter_Kmeans=niter_Kmeans)
            L1, W, weight_means, lda = lda_km(X,K,d,W,KMidxmax,niter_Kmeans=niter_Kmeans)
        
            mdl,Y,weights, outFreeY, wfInd = GMM_LDA(X,L1,d,W,GMMidxmax,niter_Kmeans=niter_Kmeans,tol=tol,excludeFun=excludeFun, noise_p = noise_p)
        except ValueError:
            if 2 in L_dict.keys():
                print 'Assign 2 clusters due to error'
                K1 = 2
            else:
                print 'Assign 1 cluster due to error'
                L_dict[1] = np.ones(X.shape[0],dtype=int) * -1
                Y_dict[1] = None
                K1 = 1
            
            break
        # DECOMMENT TO DEBUG
        plt.close('all')
        L = mdl.predict(Y)
        if np.sum(1 - wfInd):
            noise_lab = L[True-wfInd][0]
        else:
            noise_lab = np.nan
        unqL = np.unique(L)
        ii = 1
        
        for kk in unqL:
            plt.subplot(unqL.shape[0],1,ii)
            plt.plot(np.mean(X[L == kk,:],axis=0))
            plt.fill_between(np.arange(X.shape[1]),np.nanmean(X[L == kk,:],axis=0)-np.nanstd(X[L == kk,:],axis=0),np.nanmean(X[L == kk,:],axis=0)+np.nanstd(X[L == kk,:],axis=0),alpha=0.3)
            ii += 1
            if kk == noise_lab:
                plt.title('Noise class: %d'%kk)
            else:
                plt.title('Class %d'%kk)
            plt.xticks([])
        plt.savefig('debug_wf.png')
        ## end debug
        
        s0 = -np.inf
        for i in range(niter_Kmeans):
            kmeans = clust.KMeans(n_clusters=K)
            kmeans = kmeans.fit(outFreeY)
            s1 = kmeans.score(outFreeY)
            if s1 > s0:
                L = kmeans.labels_
        
        Lall = np.ones(Y.shape[0]) * -1
        Lall[wfInd] = L
        L_dict[K] = Lall
        Y_dict[K] = Y
        K1 = unimodalTest(outFreeY,L,K,K1)
        if K1 == 0:
            K1 = 1
        if K1 == 1:
            Lall[Lall != -1] = 0
            L_dict[1] = Lall
            Y_dict[1] = None
    if K1 == 0:
        K1 = 1
    return K1, L_dict[K1], Y_dict[K1]
                
        
def unimodalTest(Y,L,K,K1):
    labels = np.unique(L)
    Mu = np.zeros((labels.shape[0],Y.shape[1]))
    ii = 0
    for l in labels:
        Mu[ii,:] = np.nanmean(Y[L==l,:],axis=0)
        ii += 1
    for ii in xrange(labels.shape[0]):
        for jj in xrange(ii+1,labels.shape[0]):
            proj_ii = np.dot(Y[L == labels[ii],:],Mu[ii,:]-Mu[jj,:])
            proj_jj = np.dot(Y[L == labels[jj],:],Mu[ii,:]-Mu[jj,:])
            proj = np.hstack((proj_ii,proj_jj))
            T = sts.anderson(proj,dist='norm')[0]
            Tii = sts.anderson(proj_ii,dist='norm')[0]
            Tjj = sts.anderson(proj_jj,dist='norm')[0]
#            print labels[ii],labels[jj],T,Tii,Tjj
            if Tii >= T or Tjj>= T:
                K1 -= 1
    return K1

