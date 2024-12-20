import { Route, Routes, useNavigate } from 'react-router'
import { AuthLayout } from '../shared/ui/auth-layout'
import { LoginPage } from '../pages/login'
import { RegisterPage } from '../pages/register'
import { useEffect } from 'react'

export const Router = () => {

  const navigate = useNavigate()

  useEffect(() => {
    navigate('/login')
  }, [])

  return (
    <Routes>
      <Route element={<AuthLayout />}>
        <Route path="login" element={<LoginPage />} />
        <Route path="register" element={<RegisterPage />} />
      </Route>
    </Routes>
  )
}