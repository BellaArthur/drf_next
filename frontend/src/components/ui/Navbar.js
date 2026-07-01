'use client'

import Link from 'next/link'
import Image from 'next/image'
import { useAuth } from '@/context/AuthContext'
import Button from './Button'

export default function Navbar() {
    const { user, loading, logout, isAuthor } = useAuth()

    return (
        <nav className="bg-white border-b shadow-sm">
            <div className="max-w-5xl mx-auto px-4 py-3 flex items-center justify-between">
                <Link href="/" className="text-xl font-bold text-gray-900">
                    My Blog
                </Link>

                <div className="flex items-center gap-4">
                    {loading ? (
                        <span className="text-sm text-gray-400">Loading...</span>
                    ) : user ? (
                        <>
                            <Link
                                href="/profile"
                                className="flex items-center gap-2 hover:opacity-80 transition"
                            >
                                {user.profile?.avatar ? (
                                    <Image
                                        src={user.profile.avatar}
                                        alt={user.first_name}
                                        width={32}
                                        height={32}
                                        unoptimized={true}
                                        className="rounded-full object-cover w-8 h-8"
                                    />
                                ) : (
                                    <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-sm font-medium">
                                        {user.first_name?.[0]}{user.last_name?.[0]}
                                    </div>
                                )}
                                <span className="text-sm text-gray-600">
                                    Hi, {user.first_name}
                                </span>
                            </Link>

                            {isAuthor && (
                                <Link
                                    href="/dashboard"
                                    className="text-sm text-blue-600 hover:underline"
                                >
                                    Dashboard
                                </Link>
                            )}

                            <Button variant="secondary" onClick={logout}>
                                Logout
                            </Button>
                        </>
                    ) : (
                        <>
                            <Link href="/login" className="text-sm text-gray-700 hover:underline">
                                Login
                            </Link>
                            <Link href="/register">
                                <Button>Register</Button>
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    )
}