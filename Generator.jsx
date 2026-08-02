import { useState, useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import DashboardLayout from "../components/layout/DashboardLayout";
import PromptInput from "../components/generator/PromptInput";
import GenerationProgress from "../components/generator/GenerationProgress";
import { Sparkles, AlertCircle } from "lucide-react";
import toast from "react-hot-toast";
import { projectService } from "../services/projectService";


function Generator() {

  const navigate = useNavigate();


  const [prompt, setPrompt] = useState("");
  const [projectName, setProjectName] = useState("");

  const [isGenerating, setIsGenerating] = useState(false);

  const [progress, setProgress] = useState(0);

  const [error, setError] = useState(null);


  const progressInterval = useRef(null);



  useEffect(() => {

    return () => {

      if(progressInterval.current){
        clearInterval(progressInterval.current);
      }

    };

  }, []);




  const handleGenerate = async (e) => {

    e.preventDefault();


    if(!prompt.trim()){

      toast.error(
        "Please enter a project description"
      );

      return;

    }


    if(!projectName.trim()){

      toast.error(
        "Please enter a project name"
      );

      return;

    }



    setIsGenerating(true);

    setError(null);

    setProgress(0);



    progressInterval.current = setInterval(()=>{

      setProgress((prev)=>{

        if(prev >= 90)
          return 90;

        return prev + 10;

      });

    },500);




    try {


      const response =
        await projectService.generateProject({

          name: projectName.trim(),

          description: prompt.trim(),

          framework:"react"

        });



      setProgress(100);



      if(progressInterval.current){

        clearInterval(
          progressInterval.current
        );

      }



      toast.success(
        "Project generation started!"
      );



      setTimeout(()=>{

        navigate(
          `/projects/${response.project_id}`
        );

      },1000);



    }

    catch(err){


      if(progressInterval.current){

        clearInterval(
          progressInterval.current
        );

      }



      let message =
        "Failed to generate project";



      const detail =
        err?.response?.data?.detail;



      if(typeof detail === "string"){

        message = detail;

      }

      else if(Array.isArray(detail)){

        message =
          detail
          .map(item=>item.msg)
          .join(", ");

      }

      else if(detail){

        message =
          detail.msg ||
          JSON.stringify(detail);

      }

      else if(err.message){

        message = err.message;

      }



      setError(message);

      toast.error(message);

      setProgress(0);


    }



    finally{


      setIsGenerating(false);



      if(progressInterval.current){

        clearInterval(
          progressInterval.current
        );

      }


    }


  };





  return (

    <DashboardLayout>


      <div className="space-y-8">



        {/* Header */}

        <div>

          <div className="flex items-center gap-3 mb-2">

            <Sparkles
              className="w-8 h-8 text-blue-500"
            />


            <h1 className="text-3xl font-bold text-white">

              AI Project Generator

            </h1>


          </div>



          <p className="text-slate-400">

            Describe your project idea and let AI generate a complete application.

          </p>


        </div>





        {/* Error */}

        {error && (

          <div className="p-4 bg-red-900/20 border border-red-800 rounded-lg flex gap-3">

            <AlertCircle
              className="text-red-400"
            />


            <div>

              <p className="text-red-400 font-medium">

                Generation Failed

              </p>


              <p className="text-red-300 text-sm">

                {error}

              </p>


            </div>


          </div>

        )}






        {isGenerating && (

          <GenerationProgress
            progress={progress}
          />

        )}






        {!isGenerating && (

          <div className="grid lg:grid-cols-3 gap-8">



            <div className="lg:col-span-2">


              <PromptInput

                projectName={projectName}

                setProjectName={setProjectName}

                value={prompt}

                onChange={setPrompt}

                onSubmit={handleGenerate}

                isLoading={isGenerating}

              />




              <div className="mt-6">


                <h3 className="text-sm text-slate-300 mb-3">

                  Suggested Projects

                </h3>



                {[
                  {
                    name:"Todo App",
                    desc:"Task management application"
                  },

                  {
                    name:"Weather App",
                    desc:"Weather dashboard"
                  },

                  {
                    name:"Chat App",
                    desc:"Real time messaging"
                  },

                  {
                    name:"Portfolio",
                    desc:"Personal portfolio website"
                  }

                ].map(item=>(


                  <button

                    key={item.name}

                    onClick={()=>{

                      setProjectName(item.name);

                      setPrompt(item.desc);

                    }}

                    className="block w-full text-left p-4 mt-2 bg-slate-700 rounded-lg text-white"

                  >

                    <p className="font-medium">
                      {item.name}
                    </p>


                    <p className="text-sm text-slate-300">
                      {item.desc}
                    </p>


                  </button>


                ))}



              </div>


            </div>






            <div className="bg-slate-700/50 rounded-lg p-6">


              <h3 className="text-white font-semibold mb-3">

                Features

              </h3>


              <ul className="text-slate-300 space-y-2">

                <li>✓ Full-stack generation</li>

                <li>✓ React + FastAPI</li>

                <li>✓ Database setup</li>

                <li>✓ Authentication ready</li>

                <li>✓ Deployment ready</li>


              </ul>


            </div>



          </div>


        )}




      </div>


    </DashboardLayout>

  );

}


export default Generator;