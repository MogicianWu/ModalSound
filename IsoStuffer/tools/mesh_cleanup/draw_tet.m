close all;
[V1,F1] = readOBJ('/home/mogicianwu/Documents/test/h1.obj');
[V2,F2] = readOBJ('/home/mogicianwu/Documents/test/h2.obj');
% V1(:,1) = V1(:,1) - min(V1(:,1));
% V1(:,2) = V1(:,2) - min(V1(:,2));
% V1(:,3) = V1(:,3) - min(V1(:,3));
% V2(:,1) = V2(:,1) - min(V2(:,1));
% V2(:,2) = V2(:,2) - min(V2(:,2));
% V2(:,3) = V2(:,3) - min(V2(:,3));
hold on
axis equal;
tsurf(F1,V1);
tsurf(F2,V2);