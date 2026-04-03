import Card from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";

export default function DashboardProfile() {
    return (
        <main className="p-6 space-y-8">

            {/* Profile Header*/}
            <section className="space-y-2">
                <h1 className="text-4xl font-bold">
                    User Profile
                </h1>
                <p className="text-lg text-gray-600 p-2 max-w-6xl leading-relaxed">
                    This section provides an overview of the user profile within the
                    administrative dashboard. The information presented here is intended
                    to demonstrate how profile-related data can be organized, displayed,
                    and managed in a structured interface.
                </p>
            </section>

            {/* Profile Summary*/}
            <Card title="Profile Summary" variant="default">
                <div className="flex flex-col md:flex-row gap-6 p-6">

                    {/* Avator Details */}
                    <div className="flex-shrink-0">
                        <div className="w-24 h-24 rounded-full bg-gray-300 flex items-center justify-center text-4xl font-medium text-gray-700">
                            SA
                        </div>
                    </div>

                    {/* Basic User Details*/}
                    <div className="space-y-1 pt-2">
                        <h2 className="text-xl font-medium">
                            Sparsh Agarwal
                        </h2>
                        <p className="text-md text-gray-600">
                            Administrator
                        </p>
                        <div className="flex gap-1 mt-2">
                            <Badge variant="warning">Active</Badge>
                            <Badge variant="primary">Admin</Badge>
                        </div>
                        <p className="pt-10 text-md text-gray-800 leading-relaxed max-w-5xl">
                            The profile represents an administrative user with full access
                            privileges. In a production environment, this section would be
                            dynamically populated from a user management system and reflect
                            real-time account status and permissions.
                        </p>
                    </div>
                </div>
            </Card>

            {/* Account Details */}
            <Card title="Account Details" variant="default">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-lg p-4">
                    <div>
                        <p className="text-gray-600 text-lg border-b border-gray-400 pb-2">Email Address</p>
                        <p className="font-medium pt-2">admin_sparsh@example.com</p>
                    </div>

                    <div>
                        <p className="text-gray-600 text-lg border-b border-gray-400 pb-2">Role</p>
                        <p className="font-medium pt-2">System Administrator</p>
                    </div>

                    <div>
                        <p className="text-gray-600 text-lg border-b border-gray-400 pb-2">Account Created</p>
                        <p className="font-medium pt-2">January, 2026</p>
                    </div>

                    <div>
                        <p className="text-gray-600 text-lg border-b border-gray-400 pb-2">Last Login</p>
                        <p className="font-medium pt-2">Recently Active</p>
                    </div>
                </div>
            </Card>

            <Card title="Access & Permissions" variant="default">
                <div className="p-4 text-lg">
                    <p className="text-gray-800 leading-relaxed max-w-5xl mb-3">
                        This section outlines the access level associated with the user account.
                        Permissions define which areas of the dashboard are visible and which
                        actions can be performed. For this implementation, permissions are
                        presented as static indicators.
                    </p>
                    <ul className="list-disc list-inside text-gray-800 space-y-1">
                        <li>Full access to dashboard analytics</li>
                        <li>User and role management privileges</li>
                        <li>Configuration and system settings access</li>
                        <li>Read and write permissions across modules</li>
                    </ul>
                </div>
            </Card>

            <Card title="Profile Actions" variant="default">
                <div className="p-3 flex flex-wrap gap-2">
                    <Button variant="primary" size="md">Edit Profile</Button>
                    <Button variant="success" size="md">Change Password</Button>
                    <Button variant="danger" size="md">Deactivate Account</Button>
                </div>

                <p className="text-lg text-gray-600 px-6 pb-4 max-w-5xl leading-relaxed">
                    Action buttons are presented to indicate typical administrative
                    operations. In a fully implemented system, these actions would
                    trigger form workflows, validation checks, and backend updates.
                </p>
            </Card>

        </main>
    );
}