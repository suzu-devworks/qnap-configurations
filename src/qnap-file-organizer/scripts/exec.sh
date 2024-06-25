#!/bin/sh
base_dir=$(cd $(dirname ${0}) && pwd)
echo $base_dir

if [ $# -ne 2 ] ; then
    echo "require arguments."
    echo " usage: ${0} DEST_DIR SRC_DIR"
    exit 1
fi

dest_dir=$1
src_dir=$2 

scripts=`cat <<EOS
${base_dir}/move_photo_files.py
${base_dir}/move_other_image_files.py
EOS
`

for script in ${scripts}; do
    python ${script} -o "${dest_dir}" "${src_dir}"
done

exit 0
