import { Outlet } from 'react-router'

import s from './auth-layout.module.css'

export const AuthLayout = () => {
  return (
    <div className={s.container}>
      <div className={s.wrapper}>
        <Outlet />
      </div>
    </div>
  )
}