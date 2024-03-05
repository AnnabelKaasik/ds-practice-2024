# to create additional services with grcp_tools
 python -m grpc_tools.protoc -Iutils/pb/suggestions_service --python_out=utils/pb/suggestions_service --pyi_out=utils/pb/suggestions_service --grpc_python_out=utils/pb/suggestions_service utils/pb/suggestions_service/suggestions_service.proto

 python -m grpc_tools.protoc -Iutils/pb/fraud_detection --python_out=utils/pb/fraud_detection --pyi_out=utils/pb/fraud_detection --grpc_python_out=utils/pb/fraud_detection utils/pb/fraud_detection/fraud_detection.proto


 python -m grpc_tools.protoc -Iutils/pb/transaction_verification --python_out=utils/pb/transaction_verification --pyi_out=utils/pb/transaction_verification --grpc_python_out=utils/pb/transaction_verification utils/pb/transaction_verification/suggestions_service.proto