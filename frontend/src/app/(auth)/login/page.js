'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useAuth } from '@/context/AuthContext'
import Input from '@/components/ui/Input'
import Button from '@/components/ui/Button'

export default function LoginPage() {
    const { login } = useAuth()
    const [loading, setLoading] = useState(false)
    const [error, setError]     = useState('')
    const [form, setForm] = useState({ email: '', password: '' })

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setError('')
        setLoading(true)
        try {
            await login(form)
        } catch (err) {
            setError(
                err.response?.data?.detail || 'Invalid email or password'
            )
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="max-w-md mx-auto mt-16 p-6 bg-white rounded-lg shadow">
            <h1 className="text-2xl font-bold mb-6">Login</h1>

            <form onSubmit={handleSubmit}>
                <Input
                    label="Email"
                    name="email"
                    type="email"
                    value={form.email}
                    onChange={handleChange}
                    required
                />
                <Input
                    label="Password"
                    name="password"
                    type="password"
                    value={form.password}
                    onChange={handleChange}
                    required
                />

                {error && (
                    <p className="text-red-500 text-sm mb-4">{error}</p>
                )}

                <Button type="submit" loading={loading} className="w-full">
                    Login
                </Button>
            </form>

            <p className="text-sm text-gray-600 mt-4">
                Don&apos;t have an account?{' '}
                <Link href="/register" className="text-blue-600 hover:underline">
                    Register
                </Link>
            </p>
        </div>
    )
}