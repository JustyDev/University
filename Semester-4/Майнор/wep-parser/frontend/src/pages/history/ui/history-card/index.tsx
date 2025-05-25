import {ParseResultDto} from "@shared/api";

import s from './history-card.module.css'
import {useNavigate} from "react-router-dom";

type HistoryCardProps = {
  item: ParseResultDto
}

export const HistoryCard = ({item}: HistoryCardProps) => {
  const navigate = useNavigate()

  const onClick = () => {
    navigate('/result/' + item._id)
  }

  const toLink = (url: string) => {
    window.open(url, '_blank')
  }

  return (
    <div onClick={onClick} className={s.item}>
      <h3>Парсинг от {new Date(item.createdAt).toLocaleString()}</h3>

      <h4>Запрошенные адреса:</h4>

      <div className={s.links}>
        {item.urls.map(url => (
          <div className={s.label} onClick={(e) => {
            e.stopPropagation();
            toLink(url)
          }} title={url}>{url}</div>
        ))}
      </div>

      <h4>Обработанные адреса:</h4>

      <div className={s.links}>
        {item.results.map(result => (
          <div className={s.label} onClick={(e) => {
            e.stopPropagation();
            toLink(result.url)
          }} title={result.url}>{result.url}</div>
        ))}
      </div>
    </div>
  )
}