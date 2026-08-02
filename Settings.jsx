import DashboardLayout from "../components/layout/DashboardLayout";
import { Settings as SettingsIcon } from "lucide-react";

function Settings() {

  return (
    <DashboardLayout>

      <div className="space-y-6">

        <div className="flex items-center gap-3">

          <SettingsIcon className="w-8 h-8 text-blue-500" />

          <h1 className="text-3xl font-bold text-white">
            Settings
          </h1>

        </div>


        <div className="bg-slate-800 rounded-lg p-6">

          <h2 className="text-xl font-semibold text-white mb-4">
            Account Settings
          </h2>


          <div className="space-y-4 text-slate-300">

            <div>
              <label className="block text-sm mb-2">
                Name
              </label>

              <input
                type="text"
                placeholder="Your name"
                className="w-full p-3 rounded-lg bg-slate-700 text-white"
              />

            </div>


            <div>
              <label className="block text-sm mb-2">
                Email
              </label>

              <input
                type="email"
                placeholder="Your email"
                className="w-full p-3 rounded-lg bg-slate-700 text-white"
              />

            </div>


            <button className="btn btn-primary">
              Save Changes
            </button>


          </div>

        </div>


      </div>

    </DashboardLayout>
  );
}


export default Settings;