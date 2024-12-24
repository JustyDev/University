import {Route, Routes} from 'react-router'
import {AuthLayout} from '../shared/ui/auth-layout'
import {LoginPage} from '../pages/login'
import {RegisterPage} from '../pages/register'
import {CommonPage} from "../pages/common";

export const Router = () => {
  return (
    <Routes>
      <Route index element={<CommonPage/>}/>

      <Route element={<AuthLayout />}>
        <Route path="login" element={<LoginPage />} />
        <Route path="register" element={<RegisterPage />} />
      </Route>
    </Routes>
  )
}