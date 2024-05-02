# to create additional services with grcp_tools
 python -m grpc_tools.protoc -Iutils/pb/suggestions_service --python_out=utils/pb/suggestions_service --pyi_out=utils/pb/suggestions_service --grpc_python_out=utils/pb/suggestions_service utils/pb/suggestions_service/suggestions_service.proto

 python -m grpc_tools.protoc -Iutils/pb/fraud_detection --python_out=utils/pb/fraud_detection --pyi_out=utils/pb/fraud_detection --grpc_python_out=utils/pb/fraud_detection utils/pb/fraud_detection/fraud_detection.proto


 python -m grpc_tools.protoc -Iutils/pb/transaction_verification --python_out=utils/pb/transaction_verification --pyi_out=utils/pb/transaction_verification --grpc_python_out=utils/pb/transaction_verification utils/pb/transaction_verification/transaction_verification.proto

 python -m grpc_tools.protoc -Iutils/pb/order_queue --python_out=utils/pb/order_queue --pyi_out=utils/pb/order_queue --grpc_python_out=utils/pb/order_queue utils/pb/order_queue/order_queue.proto


 python -m grpc_tools.protoc -Iutils/pb/order_executor --python_out=utils/pb/order_executor --pyi_out=utils/pb/order_executor --grpc_python_out=utils/pb/order_executor utils/pb/order_executor/order_executor.proto

  python -m grpc_tools.protoc -Iutils/pb/database --python_out=utils/pb/database --pyi_out=utils/pb/database --grpc_python_out=utils/pb/database utils/pb/database/database.proto


 TÖÖTAB
 Book suggestions, fraud,
 
 Probleem: trans verif return, comment on sees