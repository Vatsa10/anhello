'use client'

import { useAuth } from '@/lib/auth'
import DashboardLayout from '@/components/DashboardLayout'

export default function Dashboard() {
  const { user } = useAuth()

  return (
    <DashboardLayout>
      <div className="p-6">
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">
            Welcome back, {user?.username || 'Admin'}!
          </h1>
          <p className="text-gray-600 mt-2">
            Manage your client blogs from this dashboard.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Total Clients
            </h3>
            <p className="text-3xl font-bold text-blue-600">0</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Published Posts
            </h3>
            <p className="text-3xl font-bold text-green-600">0</p>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-2">
              Draft Posts
            </h3>
            <p className="text-3xl font-bold text-yellow-600">0</p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  )
}
