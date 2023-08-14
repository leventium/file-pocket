import React from 'react';
import { useState } from 'react';

export default function Download() {
  const [downloadKey, setDownloadKey] = useState(null);

  const inpuKey = (event) => {
    setDownloadKey(event.target.value)
  };

  const handleDownload = async () => {
    if (!downloadKey) {
      alert("Введите ключ");
      return;
    };
    console.log(downloadKey);
  };

  return (
    <form action='#' className="form form_download">
                    <h3 className="form-title">Для скачивания файла введите ключ</h3>
                    <p>
                        <input type="text" onChange={inpuKey} className="form_input" placeholder="Ключ" />
                    </p>
                    <p>
                        <button onClick={handleDownload} className="form__btn form__btn_download">Скачать</button>
                    </p>
    </form>
  )
}
