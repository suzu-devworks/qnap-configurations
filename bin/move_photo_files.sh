#!/opt/bin/sh

python=/opt/bin/python3
script_base=/share/homes/admin/repos/qnap-configuration
script1=${script_base}/src/move_photo_files/move_photo_files.py
script2=${script_base}/src/move_photo_files/move_other_image_files.py

log=/share/Multimedia/logs/move-photo-files.log
src_dir=/share/Multimedia/Camera\ Uploads
dest_dir=/share/Multimedia/Photo

echo ${script1} -o "${dest_dir}" "${src_dir}"
${python} ${script1} -o "${dest_dir}" "${src_dir}" 2>&1 | tee -a ${log}

echo ${script2} -o "${dest_dir}" "${src_dir}"
${python} ${script2} -o "${dest_dir}" "${src_dir}" 2>&1 | tee -a ${log}
