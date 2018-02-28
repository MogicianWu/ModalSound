function [V,F] = meshclean(V,F)
%MESHCLEAN Summary of this function goes here
%   Detailed explanation goes here

eps = 1e-6;
[V,~,SVJ] = remove_duplicate_vertices(V,eps);
F = SVJ(F);

F = F(doublearea(V,F) > eps,:);
[V,IM] = remove_unreferenced(V,F);
 
F = IM(F);

end

