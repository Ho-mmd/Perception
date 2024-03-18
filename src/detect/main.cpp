#include <iostream>
#include <torch/torch.h>
#include <torch/script.h>
#include <opencv2/opencv.hpp>

int main() {
	
	std::string model_path = "/home/detect/models/bestn.torchscript";
	std::string image_path = "/home/detect/testImage/1.jpg";

	cv::Mat image;

	try {    
        	image = cv::imread(image_path, cv::IMREAD_COLOR);    
        	std::cout << "Image loaded successfully\n";    
    	} catch(const c10::Error& e) {    
        	std::cout << "Error loading the image\n";    
        	return -1;    
    	}

	cv::Mat input_image;

	cv::resize(image, input_image, cv::Size(640, 640));
	input_image.convertTo(input_image, CV_32F, 1.0 / 255);

	auto img_tensor = torch::from_blob(input_image.data, {1, 640, 640, 3}, torch::kF32).permute({0, 3, 1, 2});
 
    	torch::jit::script::Module model;
 
    	// Load model
    	try {
        	model = torch::jit::load(model_path);
        	std::cout << "Model loaded successfully\n";
    	} catch (const c10::Error& e) {
        	std::cerr << "Error loading the model\n";
        	return -1;
    	}
 
    	torch::NoGradGuard no_grad;
    	at::Tensor output = model.forward({img_tensor}).toTuple()->elements()[0].toTensor();
 
    	std::cout << "Inference output tensor size: " << output.sizes() << std::endl;

	float conf_threshold = 0.7;
	for (int i = 0; i < output.size(1); ++i) {
		auto detection = output[0][i];

		float x_center = detection[0].item<float>();
		float y_center = detection[1].item<float>();
		float width = detection[2].item<float>();
		float height = detection[3].item<float>();
		float conf = detection[4].item<float>();

		// [5] : traffic_sign , [6] : traffic_light
		float nonamed1 = detection[5].item<float>();
		float nonamed2 = detection[6].item<float>();

		if(i == 0)
		    std::cout << x_center << "\n" << y_center << "\n" << width << "\n" << height << "\n";

		if (conf > conf_threshold) {
		    float x1 = (x_center - width / 2);
		    float y1 = (y_center - height / 2);
		    float x2 = (x_center + width / 2);
		    float y2 = (y_center + height / 2);

		    std::cout << "Detected object with confidence " << conf << " at [" << x1 << ", " << y1 << ", " << x2 << ", " << y2 << "]\n";
		    std::cout << "ID1 " << nonamed1 << "\n" << "ID2 " << nonamed2 << "\n";
		    cv::rectangle(input_image, cv::Point(x1, y1), cv::Point(x2, y2), cv::Scalar(0, 255, 0), 2);
		}
	}

    	cv::imshow("Detection Result", input_image);
    	cv::waitKey(0);

    return 0;

}
