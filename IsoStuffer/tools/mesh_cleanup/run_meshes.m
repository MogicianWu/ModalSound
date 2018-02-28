
in_dir = '~/Downloads/Thingi10K/corner_cases/reori_meshes/';
out_dir = '~/Downloads/Thingi10K/corner_cases/cleaned_reori_meshes/';
files = dir(in_dir);
poolobj = gcp;
addAttachedFiles(poolobj,{'/home/mogicianwu/Downloads/gptoolbox/mesh/readOBJ.m',...
    '/home/mogicianwu/Downloads/gptoolbox/mesh/writeOBJ.m',...
    '/home/mogicianwu/Downloads/gptoolbox/mesh/remove_duplicate_vertices.m'
    });

parfor n = 3:length(files)
    name = files(n).name;
    fullpath = strcat(in_dir,name);
    outpath = strcat(out_dir,name);
    if exist(outpath, 'file')
        fprintf('mesh: %s exists\n',name);
        continue;
    end
    [V,F] = readOBJ(fullpath);
    [V,F] = meshclean(V,F);
    fprintf('mesh num:%d\n', n);
    fprintf('cleaned mesh: %s\n',name);
    writeOBJ(outpath, V,F);
end





