import os
from PIL import Image
import numpy as np

def energy_f(pixel):
    """
    Energy functions of pixels
    """
    grads = np.gradient(pixel)
    xgrad = grads[0]
    ygrad = grads[1]
    energy = np.linalg.norm(xgrad)+np.linalg.norm(ygrad)
    return energy

def get_mat_val(mat,i,j):
    if ((i<0) | (j<0) | (i>= mat.shape[0]) | (j>= mat.shape[1])):
        return np.infty
    return mat[i][j]

def dp(img_array):
    """
    Use DP to get energy costs of seams
    """
    size = img_array.shape
    mat = np.empty((size[0],size[1]))
    print("At width %s"%mat.shape[1])
    mat.fill(np.infty)
    
    for i in range(size[0]):
        for j in range(size[1]):
            pix_energy = energy_f(img_array[i][j])
            up = get_mat_val(mat, i-1,j-1)
            diag_left = get_mat_val(mat, i-1,j)
            diag_right = get_mat_val(mat, i-1,j+1)
            min_above = min(up, diag_left, diag_right)
            if (min_above == np.infty):
                min_above = 0
            mat[i][j] = pix_energy + min_above
    return mat

def get_seam(cost_matrix):
    seam_indices=[]
    m_len = cost_matrix.shape[0]
    rowmin = np.argmin(energy_matrix[m_len-1])
    seam_indices.append((m_len-1,rowmin))
    for i in range(m_len-2,-1,-1):
        idxvaldict = {}
        last = seam_indices[-1]
        idxvaldict[0] = get_mat_val(cost_matrix,last[0],last[1])
        idxvaldict[-1]=get_mat_val(cost_matrix,last[0],last[1]-1)
        idxvaldict[1]= get_mat_val(cost_matrix,last[0],last[1]+1)
        best_above_dict = min(idxvaldict, key=idxvaldict.get)
        seam_indices.append((i,last[1]+best_above_dict))
    return seam_indices

def remove_seam(mat,seam):
    """
    Remove seam from matrix.
    """
    new = np.empty((mat.shape[0],mat.shape[1]-1,mat.shape[2]))
    for i in seam:
        # what row in matrix
        
        curr = mat[i[0]]
        curr = np.delete(curr,i[1],axis=0)
        new[i[0]] = curr
    return new

def color_seam(mat,seam):
    """
    Color seams to be removed.
    """
    cop = mat.copy()
    red = np.array([255,0,0])
    for i in seam:
        cop[i[0],i[1]] = red
    return cop

if __name__=='__main__':
    img=Image.open('bird.jpg')

    # width to resize to
    final_width = 495
    diff = img.width-final_width
    new = np.asarray(img)
    seamlines = np.asarray(img)
    for i in range(diff):
	energy_matrix = dp(new)
	seam = get_seam(energy_matrix)
	new = remove_seam(new,seam)
	seamlines = color_seam(seamlines,seam)

    seamed = Image.fromarray(np.uint8(new))
    seamlined = Image.fromarray(np.uint8(seamlines))
    print("Saving new images (smallbirb.png, linebirb.png)")
    seamed.save('smallbirb.png')
    seamlined.save('linebirb.png')
