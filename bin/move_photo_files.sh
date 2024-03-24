#!/bin/sh

root_dir=$(cd $(dirname ${0})/../ && pwd)
# python=${root_dir}/.venv/bin/python
python=/usr/bin/python3

working_root=/mnt/Multimedia
src_dir=${working_root}/Camera\ Uploads
dest_dir=${working_root}/Photo
# log_file=${working_root}/logs/move_photo_files.log

scripts=`cat <<EOS
${root_dir}/src/move_photo_files/move_photo_files.py
${root_dir}/src/move_photo_files/move_other_image_files.py
EOS
`

for script in ${scripts}; do
    # ${python} ${script} -o "${dest_dir}" "${src_dir}" 2>&1 | tee -a ${log_file}
    ${python} ${script} -o "${dest_dir}" "${src_dir}"
done

exit 0
