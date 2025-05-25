import s from "./parse-url-item.module.css";
import clsx from "clsx";
import {ParseResultDto} from "@shared/api";
import {nanoid} from "nanoid";
import {extractHeaders} from "@/pages/result/lib/extract-headers.ts";

type ParseUrlItemProps = {
  item: ParseResultDto['results'][0]
}

export const ParseUrlItem = ({item}: ParseUrlItemProps) => {

  const isFailed = item.status_code !== 200

  const headers = extractHeaders(item.data)

  return (
    <div className={s.item}>
      <h3 className={s.title}><span className={clsx(s.lap, isFailed && s.errored)}/>Адрес: <a
        href={item.url}
        target='_blank'>{item.url.replace('https://', '').replace('http://', '')}</a>
      </h3>

      {!isFailed && (
        <>
          {item.data?.title && <p>Заголовок страницы: {item.data?.title}</p>}
          {item.data?.description && <p>Описание страницы: {item.data?.description}</p>}
          {!!item.data?.keywords?.length && <p>Ключевые слова: {item.data?.keywords.join(', ')}</p>}

          <h4>Текстовый контент</h4>

          <div className={s.labels}>
            {item.data?.textContent.map(text => (
              <span key={nanoid()} title={text} className={s.label}>{text}</span>
            ))}
          </div>

          <h4>Изображения</h4>

          <div className={s.images}>
            {item.data?.images.map(image => {
              let imageUrl = image

              if (imageUrl.startsWith('//')) {
                imageUrl = 'https:' + imageUrl
              } else if (imageUrl.startsWith('/')) {
                imageUrl = 'https://' + item.url + imageUrl
              }

              return (
                <div className={s.image} key={nanoid()} style={{
                  backgroundImage: `url(${imageUrl})`,
                }}/>
              )
            })}
          </div>

          <h4>Заголовки</h4>

          <div className={s.headers}>
            {headers.map(header => (
              <span key={nanoid()} title={header.text} className={s.label}>(H{header.level}) {header.text}</span>
            ))}
          </div>

          <h4>Внутренние ссылки</h4>

          <div className={s.links}>
            {item.data?.internalLinks.map(link => (
              <a target='_blank' href={link} key={nanoid()} title={link} className={s.label}>{link}</a>
            ))}
          </div>

          <h4>Внешние ссылки</h4>

          <div className={s.links}>
            {item.data?.externalLinks.map(link => (
              <a target='_blank' href={link} key={nanoid()} title={link} className={s.label}>{link}</a>
            ))}
          </div>
        </>
      )}

      {isFailed && (
        <>
          <p>Status code: {item.status_code}</p>
          <p>Error message: {item.error}</p>
        </>
      )}
    </div>
  )
}