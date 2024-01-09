import React from 'react';
import { useState } from 'react';

export default function Download() {
  const [downloadKey, setDownloadKey] = useState(null);

  const inpuKey = (event) => {
    setDownloadKey(event.target.value)
  };

  const handleDownload = async (e) => {
    if (!downloadKey) {
      alert("Введите ключ");
      return;
    };
    console.log(downloadKey);

    e.preventDefault();

    try{
      let response = await fetch('https://restcountries.com/v4.1/all', {
        method: 'GET',
      });

      if (response.ok) {
        alert("Файл получен");
        let data = response.blob();
        let url = URL.createObjectURL(result);
        console.log(url);

        let anchor = document.createElement('a');
        anchor.href = url;
        anchor.download;
        document.body.append(anchor);
        anchor.style = 'display: none';
        anchor.click();
        anchor.remove();
      }
      else {
        alert("Ошибка " + response.status);
      }
    } catch (error) {
      console.log("Возникла проблема с вашим fetch запросом: ", error.message);
      alert("Возникла проблема с вашим fetch запросом: ", error.message);
    };
    

    
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
