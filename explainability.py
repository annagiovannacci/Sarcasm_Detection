import numpy as np
import torch
import tensorflow as tf

def get_embeddings(input_ids,model):
  embedding_matrix = model.embeddings.word_embeddings

  vocab_size = embedding_matrix.num_embeddings
  one_hot_tensor = _one_hot(input_ids, vocab_size)
  
  one_hot_tensor = torch.from_numpy(one_hot_tensor)
  print(len(input_ids))
  print("---")
  print(one_hot_tensor)
  token_ids_tensor_one_hot = one_hot_tensor.clone().requires_grad_(True)
  # token_ids_tensor_one_hot.requires_grad_(True)

  inputs_embeds = torch.matmul(token_ids_tensor_one_hot, embedding_matrix.weight)
  return inputs_embeds, token_ids_tensor_one_hot

def to(self, tensor: torch.Tensor):
  if self.device == 'cuda':
      return tensor.to('cuda')
  return tensor

def _one_hot(token_ids, vocab_size):
    return tf.one_hot(token_ids, vocab_size).numpy()

def gradient_x_inputs_attribution(prediction_logit, inputs_embeds, retain_graph=True):

    inputs_embeds.retain_grad()
    # back-prop gradient
    prediction_logit.sum().backward(retain_graph=retain_graph)
    #grad = inputs_embeds.grad
    # This should be equivalent to
    grad = torch.autograd.grad(prediction_logit.sum(), inputs_embeds)[0]

    # Grad X Input
    grad_x_input = grad * inputs_embeds

    # Turn into a scalar value for each input token by taking L2 norm
    feature_importance = torch.norm(grad_x_input, dim=2)
    print(feature_importance)
    # Normalize so we can show scores as percentages
    token_importance_normalized = feature_importance / torch.sum(feature_importance)

    # Zero the gradient for the tensor so next backward() calls don't have
    # gradients accumulating
    inputs_embeds.grad.data.zero_()
    return token_importance_normalized
  
def saliency(prediction_logit, token_ids_tensor_one_hot, norm=True, retain_graph=True):
    # Back-propagate the gradient from the selected output-logit
    prediction_logit.sum().backward(retain_graph=retain_graph)

    # token_ids_tensor_one_hot.grad is the gradient propegated to ever embedding dimension of
    # the input tokens.
    if norm:  # norm calculates a scalar value (L2 Norm)
        token_importance_raw = torch.norm(token_ids_tensor_one_hot.grad, dim=1)
        # print('token_importance_raw', token_ids_tensor_one_hot.grad.shape,
        # np.count_nonzero(token_ids_tensor_one_hot.detach().numpy(), axis=1))

        # Normalize the values so they add up to 1
        token_importance = token_importance_raw / torch.sum(token_importance_raw)
    else:
        token_importance = torch.sum(token_ids_tensor_one_hot.grad, dim=1)  # Only one value, all others are zero

    token_ids_tensor_one_hot.grad.data.zero_()
    return token_importance