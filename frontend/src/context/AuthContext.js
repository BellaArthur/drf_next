'use client'

import { createContext, useContext, useState, useEffect } from 'react'
import Cookies from 'js-cookie'
import { useRouter } from 'next/navigation'
import toast from 'react-hot-toast'
import { authAPI } from '@/lib/api'

const AuthContext = createContext(null)

export function AuthProvider({ children }) {
    const [user, setUser]       = useState(null)
    const [loading, setLoading] = useState(true)
    const router = useRouter()

    // On first load, check if we have a token and fetch the user
    useEffect(() => {
        const loadUser = async () => {
            const access = Cookies.get('access')
            if (!access) {
                setLoading(false)
                return
            }
            try {
                const { data } = await authAPI.getMe()
                setUser(data.data)
            } catch (err) {
                Cookies.remove('access')
                Cookies.remove('refresh')
            } finally {
                setLoading(false)
            }
        }
        loadUser()
    }, [])

    const login = async (credentials) => {
        const { data } = await authAPI.login(credentials)

        Cookies.set('access',  data.access,  { secure: true, sameSite: 'strict' })
        Cookies.set('refresh', data.refresh, { secure: true, sameSite: 'strict' })

        const me = await authAPI.getMe()
        setUser(me.data.data)

        toast.success(`Welcome back, ${me.data.data.first_name}!`)
        router.push('/')
    }

    const register = async (formData) => {
        const { data } = await authAPI.register(formData)
        toast.success(data.message)
        router.push('/login')
    }

    const logout = async () => {
        const refresh = Cookies.get('refresh')
        try {
            if (refresh) {
                await authAPI.logout(refresh)
            }
        } catch (err) {
            // even if the API call fails, clear local state
        } finally {
            Cookies.remove('access')
            Cookies.remove('refresh')
            setUser(null)
            toast.success('Logged out successfully')
            router.push('/login')
        }
    }

    const isAuthor = user?.profile?.role === 'author'

    return (
        <AuthContext.Provider value={{ user, loading, login, register, logout, isAuthor }}>
            {children}
        </AuthContext.Provider>
    )
}

export function useAuth() {
    const context = useContext(AuthContext)
    if (!context) {
        throw new Error('useAuth must be used within an AuthProvider')
    }
    return context
}