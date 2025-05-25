import {PropsWithChildren} from "react";

import s from './page-layout.module.css'
import clsx from "clsx";

type PageLayoutProps = PropsWithChildren & {
  className?: string
}

export const PageLayout = ({children, className}: PageLayoutProps) => {
  return (
    <div className={s.layout}>
      <div className={clsx(s.page, className)}>
        {children}
      </div>
    </div>
  )
}